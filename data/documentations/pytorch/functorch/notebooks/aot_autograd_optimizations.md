# AOT Autograd - How to use and optimize?

<a href="https://colab.research.google.com/github/pytorch/pytorch/blob/master/functorch/notebooks/aot_autograd_optimizations.ipynb">
  <img style="width: auto" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Background
In this tutorial, we will learn how to use AOT Autograd to speedup training of deep learning models.

For background, AOT Autograd is a toolkit to assist developers in accelerating training on PyTorch. Broadly, it has two key features
* AOT Autograd traces the forward and backward graph ahead of time. Presence of forward and backward graph ahead of time facilitates joint graph optimizations such as recomputation or activation checkpointing.
* AOT Autograd provides simple mechanisms to compile the extracted forward and backward graphs through deep learning compilers, such as NVFuser, NNC, TVM and others.



## What will you learn?
In this tutorial, we will look at how AOT Autograd can be used, in conjunction with backend compilers, to accelerate the training of PyTorch models. More specifically, you will learn
* How to use AOT Autograd?
* How AOT Autograd uses backend compilers to perform operation fusion?
* How AOT Autograd enables training-specific optimizations such as Recomputation?

So, lets get started.


## Setup

Let's setup a simple model.



```python
import torch

def fn(a, b, c, d):
    x = a + b + c + d
    return x.cos().cos()
```


```python
# Test that it works
a, b, c, d = [torch.randn(2, 4, requires_grad=True) for _ in range(4)]
ref = fn(a, b, c, d)
loss = ref.sum()
loss.backward()
```

## Use AOT Autograd

Now, lets use AOT Autograd and look at the extracted forward and backward graphs. Internally, AOT uses `__torch_dispatch__` based tracing mechanism to extract forward and backward graphs, and wraps them in `torch.Fx` GraphModule containers. Note that AOT Autograd tracing is different from the usual Fx symbolic tracing. AOT Autograd uses Fx GraphModule just to represent the traced graphs (and not for tracing).

AOT Autograd then sends these forward and backward graphs to the user supplied compilers. So, lets write a compiler that just prints the graph.


```python
from functorch.compile import aot_function

# The compiler_fn is called after the forward and backward graphs are extracted.
# Here, we just print the code in the compiler_fn. Return of this function is a callable.
def compiler_fn(fx_module: torch.fx.GraphModule, _):
    print(fx_module.code)
    return fx_module

# Pass on the compiler_fn to the aot_function API
aot_print_fn = aot_function(fn, fw_compiler=compiler_fn, bw_compiler=compiler_fn)

# Run the aot_print_fn once to trigger the compilation and print the graphs
cloned_inputs = [x.clone().detach().requires_grad_(True) for x in (a, b, c, d)]
cloned_a, cloned_b, cloned_c, cloned_d = cloned_inputs
res = aot_print_fn(cloned_a, cloned_b, cloned_c, cloned_d)
res.sum().backward()
assert torch.allclose(ref, res)
```

    
    
    
    def forward(self, primals_1, primals_2, primals_3, primals_4):
        add = torch.ops.aten.add(primals_1, primals_2);  primals_1 = primals_2 = None
        add_1 = torch.ops.aten.add(add, primals_3);  add = primals_3 = None
        add_2 = torch.ops.aten.add(add_1, primals_4);  add_1 = primals_4 = None
        cos = torch.ops.aten.cos(add_2)
        cos_1 = torch.ops.aten.cos(cos)
        return [cos_1, add_2, cos]
        
    
    
    
    def forward(self, add_2, cos, tangents_1):
        sin = torch.ops.aten.sin(cos);  cos = None
        neg = torch.ops.aten.neg(sin);  sin = None
        mul = torch.ops.aten.mul(tangents_1, neg);  tangents_1 = neg = None
        sin_1 = torch.ops.aten.sin(add_2);  add_2 = None
        neg_1 = torch.ops.aten.neg(sin_1);  sin_1 = None
        mul_1 = torch.ops.aten.mul(mul, neg_1);  mul = neg_1 = None
        return [mul_1, mul_1, mul_1, mul_1]
        


The above code prints the Fx graph for the forward and backward graph. You can see that in addition to the original input of the forward pass, the forward graph outputs some additional tensors. These tensors are saved for the backward pass for gradient calculation. We will come back to these later while talking about recomputation.

## Operator Fusion
Now that we understand how to use AOT Autograd to print forward and backward graphs, let us use AOT Autograd to use some actual deep learning compiler. In this tutorial, we use PyTorch Neural Network Compiler (NNC) to perform pointwise operator fusion for CPU devices. For CUDA devices, a suitable alternative is NvFuser. So, lets use NNC


```python
# AOT Autograd has a suite of already integrated backends. Lets import the NNC compiler backend - ts_compile
from functorch.compile import ts_compile

# Lets compile the forward and backward through ts_compile.
aot_nnc_fn = aot_function(fn, fw_compiler=ts_compile, bw_compiler=ts_compile)

# Correctness checking. Lets clone the input so that we can check grads.
cloned_inputs = [x.clone().detach().requires_grad_(True) for x in (a, b, c, d)]
cloned_a, cloned_b, cloned_c, cloned_d = cloned_inputs

res = aot_nnc_fn(*cloned_inputs)
loss = res.sum()
loss.backward()
assert torch.allclose(ref, res)
assert torch.allclose(a.grad, cloned_a.grad)
assert torch.allclose(b.grad, cloned_b.grad)
assert torch.allclose(c.grad, cloned_c.grad)
assert torch.allclose(d.grad, cloned_d.grad)
```

Lets benchmark the original and AOT Autograd + NNC compiled function.


```python
# Lets write a function to benchmark the forward and backward pass
import time
import statistics

def bench(fn, args, prefix):
    warmup = 10
    iterations = 100

    for _ in range(warmup):
        ref = fn(*args)
        ref.sum().backward()
    
    fw_latencies = []
    bw_latencies = []
    for _ in range(iterations):
        for arg in args:
            arg.grad = None

        fw_begin = time.perf_counter()
        ref = fn(*args)
        fw_end = time.perf_counter()

        loss = ref.sum() 

        bw_begin = time.perf_counter()
        loss.backward()
        bw_end = time.perf_counter()

        fw_latencies.append(fw_end - fw_begin)
        bw_latencies.append(bw_end - bw_begin)
    
    avg_fw_latency = statistics.mean(fw_latencies) * 10**6
    avg_bw_latency = statistics.mean(bw_latencies) * 10**6
    print(prefix, "Fwd = " + str(avg_fw_latency) + " us", "Bwd = " + str(avg_bw_latency) + " us", sep=', ')

```


```python
large_inputs = [torch.randn(1024, 2048, requires_grad=True) for _ in range(4)]

# Benchmark the Eager and AOT Autograd functions
bench(fn, large_inputs, "Eager")
bench(aot_nnc_fn, large_inputs, "AOT")
```

    Eager, Fwd = 982.6959593920038 us, Bwd = 1899.7003795811906 us
    AOT, Fwd = 734.2723174951971 us, Bwd = 831.1696897726506 us


With the help of NNC, AOT Autograd speeds up both the forward and backward pass. If we look at the printed graphs earlier, all the operators are pointwise. The pointwise operators are memory bandwidth bound, and thus benefit from operator fusion. Looking closely at the numbers, the backward pass gets higher speedup. This is because forward pass has to output some intermediate tensors for gradient calculation for the backward pass, preventing it from saving some memory reads and writes. However, such restriction does not exist in the backward graph.

## Recomputation (aka Activation Checkpointing)
Recomputation (often called activation checkpointing) is a technique in which, instead of saving some activations for use in backwards, we recompute them **during** the backwards pass. Recomputing saves memory, but we incur performance overhead.

However, in the presence of fusing compiler, we can do better than that. We can recompute the fusion-friendly operators to save memory, and then rely on the fusing compiler to fuse the recomputed operators. This reduces both memory and runtime. Please refer to this [discuss post](https://dev-discuss.pytorch.org/t/min-cut-optimal-recomputation-i-e-activation-checkpointing-with-aotautograd/467) for more details.

Here, we use AOT Autograd with NNC to perform similar type of recomputation. At the end of `__torch_dispatch__` tracing, AOT Autograd has a forward graph and joint forward-backward graph. AOT Autograd then uses a partitioner to isolate the forward and backward graph. In the example above, we used a default partitioner. For this experiment, we will use another partitioner called `min_cut_rematerialization_partition` to perform smarter fusion-aware recomputation. The partitioner is configurable and one can write their own partitioner to plug it in AOT Autograd.


```python
from functorch.compile import min_cut_rematerialization_partition

# Zero out the gradients so we can do a comparison later
a.grad, b.grad, c.grad, d.grad = (None,) * 4

# Lets set up the partitioner. Also set the fwd and bwd compilers to the printer function that we used earlier.
# This will show us how the recomputation has modified the graph.
aot_fn = aot_function(fn, fw_compiler=compiler_fn, bw_compiler=compiler_fn, partition_fn=min_cut_rematerialization_partition)
res = aot_fn(a, b, c, d).sum().backward()
```

    
    
    
    def forward(self, primals_1, primals_2, primals_3, primals_4):
        add = torch.ops.aten.add(primals_1, primals_2);  primals_1 = primals_2 = None
        add_1 = torch.ops.aten.add(add, primals_3);  add = primals_3 = None
        add_2 = torch.ops.aten.add(add_1, primals_4);  add_1 = primals_4 = None
        cos = torch.ops.aten.cos(add_2)
        cos_1 = torch.ops.aten.cos(cos);  cos = None
        return [cos_1, add_2]
        
    
    
    
    def forward(self, add_2, tangents_1):
        cos = torch.ops.aten.cos(add_2)
        sin = torch.ops.aten.sin(cos);  cos = None
        neg = torch.ops.aten.neg(sin);  sin = None
        mul = torch.ops.aten.mul(tangents_1, neg);  tangents_1 = neg = None
        sin_1 = torch.ops.aten.sin(add_2);  add_2 = None
        neg_1 = torch.ops.aten.neg(sin_1);  sin_1 = None
        mul_1 = torch.ops.aten.mul(mul, neg_1);  mul = neg_1 = None
        return [mul_1, mul_1, mul_1, mul_1]
        


We can see that compared to default partitioner, forward pass now outputs fewer tensors, and recomputes some operations in the backward pass. Let us try NNC compiler now to perform operator fusions (note that we also have a wrapper function - `memory_efficient_fusion` which internally uses `min_cut_rematerialization_partition` and Torchscript compiler to achieve the same effect as following code).


```python

# Lets set up the partitioner and NNC compiler.
aot_recompute_nnc_fn = aot_function(fn, fw_compiler=ts_compile, bw_compiler=ts_compile, partition_fn=min_cut_rematerialization_partition)

# Correctness checking. Lets clone the input so that we can check grads.
cloned_inputs = [x.clone().detach().requires_grad_(True) for x in (a, b, c, d)]
cloned_a, cloned_b, cloned_c, cloned_d = cloned_inputs

res = aot_recompute_nnc_fn(*cloned_inputs)
loss = res.sum()
loss.backward()
assert torch.allclose(ref, res)
assert torch.allclose(a.grad, cloned_a.grad)
assert torch.allclose(b.grad, cloned_b.grad)
assert torch.allclose(c.grad, cloned_c.grad)
assert torch.allclose(d.grad, cloned_d.grad)
```

Finally, lets benchmark the different functions


```python
bench(fn, large_inputs, "Eager")
bench(aot_nnc_fn, large_inputs, "AOT")
bench(aot_recompute_nnc_fn, large_inputs, "AOT_Recomp")
```

    Eager, Fwd = 740.7676504226401 us, Bwd = 1560.5240693548694 us
    AOT, Fwd = 713.8530415249988 us, Bwd = 909.1200679540634 us
    AOT_Recomp, Fwd = 712.2249767417088 us, Bwd = 791.4606417762116 us


We observe that both forward and backward latency improve over the default partitioner (and a lot better than eager). Fewer outputs in the forward pass and fewer inputs in the backward pass, along with fusion, allows better memory bandwidth utilization leading to further speedups.

## Actual Usage
For actual usage on CUDA devices, we've wrapped AOTAutograd in a convenient wrapper - `memory_efficient_fusion`. Use this for fusion on GPU!

```
from functorch.compile import memory_efficient_fusion
```

