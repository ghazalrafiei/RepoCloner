# Jacobians, Hessians, hvp, vhp, and more: composing functorch transforms

<a href="https://colab.research.google.com/github/pytorch/pytorch/blob/master/functorch/notebooks/jacobians_hessians.ipynb">
  <img style="width: auto" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Computing jacobians or hessians are useful in a number of non-traditional
deep learning models. It is difficult (or annoying) to compute these quantities
efficiently using a standard autodiff system like PyTorch Autograd; functorch
provides ways of computing various higher-order autodiff quantities efficiently.

## Computing the Jacobian


```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from functools import partial
_ = torch.manual_seed(0)
```

Let’s start with a function that we’d like to compute the jacobian of.  This is a simple linear function with non-linear activation.




```python
def predict(weight, bias, x):
    return F.linear(x, weight, bias).tanh()
```

Let's add some dummy data:   a weight, a bias, and a feature vector x.




```python
D = 16
weight = torch.randn(D, D)
bias = torch.randn(D)
x = torch.randn(D) # feature vector
```

Let's think of `predict` as a function that maps the input `x` from $R^D -> R^D$.
PyTorch Autograd computes vector-Jacobian products. In order to compute the full
Jacobian of this $R^D -> R^D$ function, we would have to compute it row-by-row
by using a different unit vector each time.


```python
def compute_jac(xp):
    jacobian_rows = [torch.autograd.grad(predict(weight, bias, xp), xp, vec)[0]
                     for vec in unit_vectors]
    return torch.stack(jacobian_rows)
```


```python
xp = x.clone().requires_grad_()
unit_vectors = torch.eye(D)

jacobian = compute_jac(xp)

print(jacobian.shape)
print(jacobian[0])  # show first row
```

    torch.Size([16, 16])
    tensor([-0.5956, -0.6096, -0.1326, -0.2295,  0.4490,  0.3661, -0.1672, -1.1190,
             0.1705, -0.6683,  0.1851,  0.1630,  0.0634,  0.6547,  0.5908, -0.1308])


Instead of computing the jacobian row-by-row, we can use vmap to get rid of the for-loop and vectorize the computation. 
We can’t directly apply vmap to PyTorch Autograd; instead, functorch provides a vjp transform:




```python
from functorch import vmap, vjp

_, vjp_fn = vjp(partial(predict, weight, bias), x)

ft_jacobian, = vmap(vjp_fn)(unit_vectors)

# lets confirm both methods compute the same result
assert torch.allclose(ft_jacobian, jacobian)
```

In future tutorial a composition of reverse-mode AD and vmap will give us per-sample-gradients. 
In this tutorial, composing reverse-mode AD and vmap gives us Jacobian computation! 
Various compositions of vmap and autodiff transforms can give us different interesting quantities.

functorch provides **jacrev** as a convenience function that performs the vmap-vjp composition to compute jacobians. **jacrev** accepts an argnums argument that says which argument we would like to compute Jacobians with respect to.




```python
from functorch import jacrev

ft_jacobian = jacrev(predict, argnums=2)(weight, bias, x)

# confirm 
assert torch.allclose(ft_jacobian, jacobian)
```

Let’s compare the performance of the two ways to compute the jacobian. The functorch version is much faster (and becomes even faster the more outputs there are). 

In general, we expect that vectorization via vmap can help eliminate overhead and give better utilization of your hardware.

Vmap does this magic by pushing the outer loop down into the functions primitive operations in order to obtain better performance.




Let's make a quick function to evaluate performance and deal with microseconds and milliseconds measurements:


```python
def get_perf(first, first_descriptor, second, second_descriptor):
  """  takes torch.benchmark objects and compares delta of second vs first. """
  faster = second.times[0]
  slower = first.times[0]
  gain = (slower-faster)/slower
  if gain < 0: gain *=-1 
  final_gain = gain*100
  print(f" Performance delta: {final_gain:.4f} percent improvement with {second_descriptor} ")
```

And then run the performance comparison:


```python
from torch.utils.benchmark import Timer

without_vmap = Timer(stmt="compute_jac(xp)", globals=globals())
with_vmap = Timer(stmt="jacrev(predict, argnums=2)(weight, bias, x)", globals=globals())

no_vmap_timer = without_vmap.timeit(500)
with_vmap_timer = with_vmap.timeit(500)

print(no_vmap_timer)
print(with_vmap_timer)
```

    <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a911b350>
    compute_jac(xp)
      2.25 ms
      1 measurement, 500 runs , 1 thread
    <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a6a99d50>
    jacrev(predict, argnums=2)(weight, bias, x)
      884.34 us
      1 measurement, 500 runs , 1 thread


Lets do a relative performance comparison of the above with our get_perf function:


```python
get_perf(no_vmap_timer, "without vmap",  with_vmap_timer, "vmap");
```

     Performance delta: 60.7170 percent improvement with vmap 


Furthemore, it’s pretty easy to flip the problem around and say we want to compute Jacobians of the parameters to our model (weight, bias) instead of the input.


```python
# note the change in input via argnums params of 0,1 to map to weight and bias
ft_jac_weight, ft_jac_bias = jacrev(predict, argnums=(0, 1))(weight, bias, x)
```

## reverse-mode Jacobian (jacrev) vs forward-mode Jacobian (jacfwd)


We offer two APIs to compute jacobians: **jacrev** and **jacfwd**: 
- jacrev uses reverse-mode AD. As you saw above it is a composition of our vjp and vmap transforms. 
- jacfwd uses forward-mode AD. It is implemented as a composition of our jvp and vmap transforms. 

jacfwd and jacrev can be substituted for each other but they have different performance characteristics.

As a general rule of thumb, if you’re computing the jacobian of an $𝑅^N \to R^M$ function, and there are many more outputs than inputs (i.e. $M > N$) then jacfwd is preferred, otherwise use jacrev. There are exceptions to this rule, but a non-rigorous argument for this follows:

In reverse-mode AD, we are computing the jacobian row-by-row, while in forward-mode AD (which computes Jacobian-vector products), we are computing it column-by-column. The Jacobian matrix has M rows and N columns, so if it is taller or wider one way we may prefer the method that deals with fewer rows or columns.




```python
from functorch import jacrev, jacfwd
```

First, let's benchmark with more inputs than outputs:




```python
Din = 32
Dout = 2048
weight = torch.randn(Dout, Din)

bias = torch.randn(Dout)
x = torch.randn(Din)

# remember the general rule about taller vs wider...here we have a taller matrix:
print(weight.shape)

using_fwd = Timer(stmt="jacfwd(predict, argnums=2)(weight, bias, x)", globals=globals())
using_bwd = Timer(stmt="jacrev(predict, argnums=2)(weight, bias, x)", globals=globals())

jacfwd_timing = using_fwd.timeit(500)
jacrev_timing = using_bwd.timeit(500)

print(f'jacfwd time: {jacfwd_timing}')
print(f'jacrev time: {jacrev_timing}')

```

    torch.Size([2048, 32])
    jacfwd time: <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a5d792d0>
    jacfwd(predict, argnums=2)(weight, bias, x)
      1.32 ms
      1 measurement, 500 runs , 1 thread
    jacrev time: <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a4dee450>
    jacrev(predict, argnums=2)(weight, bias, x)
      12.46 ms
      1 measurement, 500 runs , 1 thread


and then do a relative benchmark:


```python
get_perf(jacfwd_timing, "jacfwd", jacrev_timing, "jacrev", );
```

     Performance delta: 842.8274 percent improvement with jacrev 


and now the reverse - more outputs (M) than inputs (N):


```python
Din = 2048
Dout = 32
weight = torch.randn(Dout, Din)
bias = torch.randn(Dout)
x = torch.randn(Din)

using_fwd = Timer(stmt="jacfwd(predict, argnums=2)(weight, bias, x)", globals=globals())
using_bwd = Timer(stmt="jacrev(predict, argnums=2)(weight, bias, x)", globals=globals())

jacfwd_timing = using_fwd.timeit(500)
jacrev_timing = using_bwd.timeit(500)

print(f'jacfwd time: {jacfwd_timing}')
print(f'jacrev time: {jacrev_timing}')
```

    jacfwd time: <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a5d64790>
    jacfwd(predict, argnums=2)(weight, bias, x)
      7.99 ms
      1 measurement, 500 runs , 1 thread
    jacrev time: <torch.utils.benchmark.utils.common.Measurement object at 0x7fa9a5d67b50>
    jacrev(predict, argnums=2)(weight, bias, x)
      1.09 ms
      1 measurement, 500 runs , 1 thread


and a relative perf comparison:


```python
get_perf(jacrev_timing, "jacrev", jacfwd_timing, "jacfwd")
```

     Performance delta: 635.2095 percent improvement with jacfwd 


## Hessian computation with functorch.hessian


We offer a convenience API to compute hessians: `functorch.hessian`. 
Hessians are the jacobian of the jacobian (or the partial derivative of the partial derivative, aka second order).

This suggests that one can just compose functorch’s jacobian transforms to compute the Hessian. 
Indeed, under the hood, `hessian(f)` is simply `jacfwd(jacrev(f))`.



Note: to boost performance: depending on your model, you may also want to use `jacfwd(jacfwd(f))` or `jacrev(jacrev(f))` instead to compute hessians leveraging the rule of thumb above regarding wider vs taller matrices.




```python
from functorch import hessian

# lets reduce the size in order not to blow out colab. Hessians require significant memory:
Din = 512
Dout = 32
weight = torch.randn(Dout, Din)
bias = torch.randn(Dout)
x = torch.randn(Din)

hess_api = hessian(predict, argnums=2)(weight, bias, x)
hess_fwdfwd = jacfwd(jacfwd(predict, argnums=2), argnums=2)(weight, bias, x)
#hess_revrev = jacrev(jacrev(predict, argnums=2), argnums=2)(weight, bias, x)

```

Let's verify we have the same result regardless of using hessian api or using jacfwd(jacfwd())


```python
torch.allclose(hess_api, hess_fwdfwd)
```




    True



## Batch Jacobian and Batch Hessian


In the above examples we’ve been operating with a single feature vector. In some cases you might want to take the Jacobian of a batch of outputs with respect to a batch of inputs. That is, given a batch of inputs of shape `(B, N)` and a function that goes from $R^N \to R^M$, we would like a Jacobian of shape `(B, M, N)`. 

The easiest way to do this is to use vmap:


```python
batch_size = 64
Din = 31
Dout = 33

weight = torch.randn(Dout, Din)
print(f"weight shape = {weight.shape}")

bias = torch.randn(Dout)

x = torch.randn(batch_size, Din)
```

    weight shape = torch.Size([33, 31])



```python
compute_batch_jacobian = vmap(jacrev(predict, argnums=2), in_dims=(None, None, 0))
batch_jacobian0 = compute_batch_jacobian(weight, bias, x)
```

If you have a function that goes from (B, N) -> (B, M) instead and are certain that each input produces an independent output, then it’s also sometimes possible to do this without using vmap by summing the outputs and then computing the Jacobian of that function:




```python
def predict_with_output_summed(weight, bias, x):
    return predict(weight, bias, x).sum(0)

batch_jacobian1 = jacrev(predict_with_output_summed, argnums=2)(weight, bias, x).movedim(1, 0)
assert torch.allclose(batch_jacobian0, batch_jacobian1)
```

If you instead have a function that goes from $𝑅^𝑁 \to 𝑅^𝑀$ but inputs that are batched, you compose vmap with jacrev to compute batched jacobians:

Finally, batch hessians can be computed similarly. It’s easiest to think about them by using vmap to batch over hessian computation, but in some cases the sum trick also works.




```python
compute_batch_hessian = vmap(hessian(predict, argnums=2), in_dims=(None, None, 0))

batch_hess = compute_batch_hessian(weight, bias, x)
batch_hess.shape
```




    torch.Size([64, 33, 31, 31])



## Computing Hessian-vector products

The naive way to compute a Hessian-vector product (hvp) is to materialize the full Hessian and perform a dot-product with a vector. We can do better: it turns out we don't need to materialize the full Hessian to do this. We'll go through two (of many) different strategies to compute Hessian-vector products:
- composing reverse-mode AD with reverse-mode AD
- composing reverse-mode AD with forward-mode AD

Composing reverse-mode AD with forward-mode AD (as opposed to reverse-mode with reverse-mode) is generally the more memory efficient way to compute a hvp because forward-mode AD doesn't need to construct an Autograd graph and save intermediates for backward:


```python
from functorch import jvp, grad, vjp

def hvp(f, primals, tangents):
  return jvp(grad(f), primals, tangents)[1]
```

Here's some sample usage.


```python
def f(x):
  return x.sin().sum()

x = torch.randn(2048)
tangent = torch.randn(2048)

result = hvp(f, (x,), (tangent,))
```

If PyTorch forward-AD does not have coverage for your operations, then we can instead compose reverse-mode AD with reverse-mode AD:


```python
def hvp_revrev(f, primals, tangents):
  _, vjp_fn = vjp(grad(f), *primals)
  return vjp_fn(*tangents)
```


```python
result_hvp_revrev = hvp_revrev(f, (x,), (tangent,))
assert torch.allclose(result, result_hvp_revrev[0])
```
