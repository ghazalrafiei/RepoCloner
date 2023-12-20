# Using the Minifier
We have a pretty convenient test case minifier with this interface
```
def minifier(fail_f: fx.GraphModule, inps, module_fails):
    """
    Minimizes a FX graph with given inputs, such that the resulting FX graph still returns True for module_fails.

    Does 2 main strategies:
    1. Truncates suffix: Removes some suffix from the graph and sets a new output.
    2. Delta Debugging: Tries replacing half of the graph with inputs. If fails,
        tries replacing quarter of the graph, etc.

    >>> failing_function = fx.symbolic_trace(f)
    >>> minimize(failing_function, [torch.randn(5)], lambda fx_g, inps: fx_g(*inps))

    note: module_fails returns True if it fails.
    ...
```

Specifically, it takes your FX graph, and tries to minify it with the following 4 strategies (while checking that the resulting graph still returns True for `module_fails`), until it can't minify it anymore.

1. Truncates Suffix: Given a FX graph, it tries to remove some suffix from the graph. For example, given this:

```
def f(a):
    b = x * 2
    c = b + 3
    d = c / 4
    return d
```
It might try truncating the suffix, and get
```
def f(a):
    b = x * 2
    c = b + 3
    return c
```
It tries this in a binary search manner, trying to remove the last 1/2, then 3/4, 1/4 then 7/8, 5/8, 3/8...

2. [Delta Debugging](https://en.wikipedia.org/wiki/Delta_debugging): Of course, removing the suffix isn't always sufficient to minify a graph. What if the error is caused by the first instruction? So, we take an approach inspired by delta debugging - we try removing intermediate nodes of the graph. Unlike with suffixes, there are still dependencies on the removed nodes. So, instead of removing them entirely, we promote them to inputs. For example, given the above example:

```
def f(a):
    b = x * 2
    c = b + 3
    d = c / 4
    return d
```
We might remove a middle node (say, c, in this case).
```
def f(a, c):
    b = x * 2
    d = c / 4
    return d
```

Finally, there are 2 auxiliary strategies - eliminating dead code and removing unused inputs. These are somewhat self-explanatory.

So, let's take a look at a toy example. Let's pretend that our graph fails if it has a "multiply" in it. Let's create a failing graph.


```python
import torch
import torch.fx as fx
from functorch.compile import minifier

def failing_f(x, y):
    y = torch.ops.aten.div(x, y)
    x = torch.ops.aten.add(x, 3)
    x = torch.ops.aten.mul(x, y)
    return torch.ops.aten.sub(x, y)

inps = [torch.randn(3), torch.randn(3)]

def pass_checker(fx_g, inps):
    return (torch.ops.aten.mul in set([i.target for i in fx_g.graph.nodes]))

min_f, inps = minifier(fx.symbolic_trace(failing_f), inps, pass_checker)
```

    [W OperatorEntry.cpp:133] Warning: Overriding a previously registered kernel for the same operator and the same dispatch key
      operator: aten::multiply.Tensor(Tensor self, Tensor other) -> (Tensor)
        registered at aten/src/ATen/RegisterSchema.cpp:6
      dispatch key: FuncTorchBatched
      previous kernel: registered at aten/src/ATen/RegisterCompositeImplicitAutograd.cpp:10338
           new kernel: registered at /fsx/users/chilli/work/functorch/functorch/csrc/BatchRulesDecompositions.cpp:108 (function registerKernel)


    Started off with 7 nodes
    ###################
    Current size: 7
    ###################
    Strategy: Remove suffix
    
    SUCCESS: Removed [4:7)
    
    ###################
    Current size: 6
    ###################
    Strategy: Delta Debugging
    SUCCESS: Removed (0:4] - Went from 2 placeholders to 4
    
    ###################
    Current size: 6
    ###################
    Strategy: Remove unused inputs
    SUCCESS: Went from 4 inputs to 2 inputs
    
    ###################
    Current size: 4
    ###################
    Strategy: Remove suffix
    FAIL: Could not remove suffix
    Strategy: Delta Debugging
    FAIL: Could not remove prefix
    
    inps = [(torch.Size([3]), torch.float32), (torch.Size([3]), torch.float32)]
    inps = [torch.zeros(())] + [torch.ones(shape, dtype=dtype, device='cuda') for (shape, dtype) in inps]
    
    
    
    def forward(self, div, add):
        mul = torch.ops.aten.mul(add, div);  add = div = None
        return (mul,)
        
    f = torch.jit.script(forward)
    with torch.jit.fuser("fuser2"):
      for _ in range(5):
        f(*inps)


Tada! Our graph is now a minimal example that still fails.

Since the primary use case of this minifier (for now) is for NVFuser repros, we print out a string for convenience that creates a self-contained repro to run the minified graph with NVFuser.

Note that in practice, we provide 2 main "graph checkers" - `check_nvfuser_subprocess` and `check_nvfuser_correctness_subprocess`. These are used to check for errors and correctness (i.e. do the results match eager) respectively. These can be used like

```
from functorch.compile import minifier, check_nvfuser_subprocess, check_nvfuser_correctness_subprocess
minifier(failing_graph, inps, check_nvfuser_subprocess)
```

However, assuming you're using AOTAutograd, there's another problem - how do you obtain the FX graph in the first place to pass to the minifier? One possible way is simply to use `print_compile`.


```python
from functorch.compile import aot_function

from functorch.compile import print_compile
# Or...
def print_compile(fx_g, _):
    print(fx_g.code)
    return fx_g

def foo(x):
    return x.cos().cos()
inp = torch.randn(3, requires_grad=True)
aot_function(foo, print_compile)(inp)
```

    
    
    
    def forward(self, primals_1):
        cos = torch.ops.aten.cos(primals_1)
        cos_1 = torch.ops.aten.cos(cos)
        return [cos_1, primals_1, cos]
        
    
    
    
    def forward(self, primals_1, cos, tangents_1):
        sin = torch.ops.aten.sin(cos);  cos = None
        neg = torch.ops.aten.neg(sin);  sin = None
        mul = torch.ops.aten.mul(tangents_1, neg);  tangents_1 = neg = None
        sin_1 = torch.ops.aten.sin(primals_1);  primals_1 = None
        neg_1 = torch.ops.aten.neg(sin_1);  sin_1 = None
        mul_1 = torch.ops.aten.mul(mul, neg_1);  mul = neg_1 = None
        return [mul_1]
        





    tensor([0.6062, 0.9982, 0.6474], grad_fn=<CompiledFunctionBackward>)



However, this doesn't provide the inputs, nor does it handle any tensor constants that might be saved in the graph. To resolve this, we have another "compiler" called `debug_compile`. It simply prints out a string that can be copy pasted and run from another file. It leverages FX's `to_folder` feature to serialize the graph to disk, along with any constants.

You can apply it to either the `fw_compiler` to dump the forwards graph or `bw_compiler` to dump the backwards graph.


```python
from functorch.compile import memory_efficient_fusion, debug_compile

memory_efficient_fusion(foo, bw_compiler=debug_compile)(inp)

```

    
    ##############################################################
    # To minimize FX graph, copy and paste the below and run it  #
    ##############################################################
    
    import torch
    import torch.fx as fx
    from functorch.compile import minifier, check_nvfuser_subprocess, check_nvfuser_correctness_subprocess
    
    inps = [(torch.Size([3]), torch.float32), (torch.Size([3]), torch.float32)]
    inps = [torch.ones(shape, dtype=dtype, device='cuda') for (shape, dtype) in inps]
    from foo import FxModule
    mod = FxModule().cuda()
    
    with torch.jit.fuser("fuser2"):
      # check_nvfuser_subprocess can be replaced with check_nvfuser_correctness_subprocess
      minifier(fx.symbolic_trace(mod), inps, check_nvfuser_subprocess)
    





    tensor([0.6062, 0.9982, 0.6474], grad_fn=<CompiledFunctionBackward>)



So, let's copy paste it and see how it works - note that I made a couple minor modifications to run on CPU and use the previous "graph fails if there's a multiply in it" checker.


```python
import torch
import torch.fx as fx
from functorch.compile import minifier, check_nvfuser_subprocess, check_nvfuser_correctness_subprocess

inps = [(torch.Size([3]), torch.float32), (torch.Size([3]), torch.float32)]
inps = [torch.ones(shape, dtype=dtype) for (shape, dtype) in inps]
from foo import FxModule
mod = FxModule()

minifier(fx.symbolic_trace(mod), inps, pass_checker)
```

    Started off with 10 nodes
    ###################
    Current size: 10
    ###################
    Strategy: Remove suffix
    
    SUCCESS: Removed [6:10)
    
    ###################
    Current size: 8
    ###################
    Strategy: Delta Debugging
    SUCCESS: Removed (0:4] - Went from 2 placeholders to 4
    
    ###################
    Current size: 8
    ###################
    Strategy: Remove unused inputs
    SUCCESS: Went from 4 inputs to 3 inputs
    
    ###################
    Current size: 7
    ###################
    Strategy: Remove suffix
    
    SUCCESS: Removed [4:7)
    
    ###################
    Current size: 6
    ###################
    Strategy: Remove unused inputs
    SUCCESS: Went from 3 inputs to 2 inputs
    
    ###################
    Current size: 5
    ###################
    Strategy: Delta Debugging
    SUCCESS: Removed (2:3] - Went from 2 placeholders to 3
    
    ###################
    Current size: 5
    ###################
    Strategy: Remove unused inputs
    SUCCESS: Went from 3 inputs to 2 inputs
    
    ###################
    Current size: 4
    ###################
    Strategy: Remove suffix
    FAIL: Could not remove suffix
    Strategy: Delta Debugging
    FAIL: Could not remove prefix
    
    inps = [(torch.Size([3]), torch.float32), (torch.Size([3]), torch.float32)]
    inps = [torch.zeros(())] + [torch.ones(shape, dtype=dtype, device='cuda') for (shape, dtype) in inps]
    
    
    
    def forward(self, tangents_1, neg):
        mul = torch.ops.aten.mul(tangents_1, neg);  tangents_1 = neg = None
        return (mul,)
        
    f = torch.jit.script(forward)
    with torch.jit.fuser("fuser2"):
      for _ in range(5):
        f(*inps)





    (GraphModule(), [tensor([1., 1., 1.]), tensor([-0.5144, -0.5144, -0.5144])])



Hopefully that was useful :)
