# Whirlwind Tour

<a href="https://colab.research.google.com/github/pytorch/pytorch/blob/master/functorch/notebooks/whirlwind_tour.ipynb">
  <img style="width: auto" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## What is functorch?

functorch is a library for [JAX](https://github.com/google/jax)-like composable function transforms in PyTorch.
- A "function transform" is a higher-order function that accepts a numerical function and returns a new function that computes a different quantity.
- functorch has auto-differentiation transforms (`grad(f)` returns a function that computes the gradient of `f`), a vectorization/batching transform (`vmap(f)` returns a function that computes `f` over batches of inputs), and others.
- These function transforms can compose with each other arbitrarily. For example, composing `vmap(grad(f))` computes a quantity called per-sample-gradients that stock PyTorch cannot efficiently compute today.

Furthermore, we also provide an experimental compilation transform in the `functorch.compile` namespace. Our compilation transform, named AOT (ahead-of-time) Autograd, returns to you an [FX graph](https://pytorch.org/docs/stable/fx.html) (that optionally contains a backward pass), of which compilation via various backends is one path you can take.


## Why composable function transforms?
There are a number of use cases that are tricky to do in PyTorch today:
- computing per-sample-gradients (or other per-sample quantities)
- running ensembles of models on a single machine
- efficiently batching together tasks in the inner-loop of MAML
- efficiently computing Jacobians and Hessians
- efficiently computing batched Jacobians and Hessians

Composing `vmap`, `grad`, `vjp`, and `jvp` transforms allows us to express the above without designing a separate subsystem for each.

## What are the transforms?

### grad (gradient computation)

`grad(func)` is our gradient computation transform. It returns a new function that computes the gradients of `func`. It assumes `func` returns a single-element Tensor and by default it computes the gradients of the output of `func` w.r.t. to the first input.


```python
import torch
from functorch import grad
x = torch.randn([])
cos_x = grad(lambda x: torch.sin(x))(x)
assert torch.allclose(cos_x, x.cos())

# Second-order gradients
neg_sin_x = grad(grad(lambda x: torch.sin(x)))(x)
assert torch.allclose(neg_sin_x, -x.sin())
```

### vmap (auto-vectorization)

Note: vmap imposes restrictions on the code that it can be used on. For more details, please read its docstring.

`vmap(func)(*inputs)` is a transform that adds a dimension to all Tensor operations in `func`. `vmap(func)` returns a new function that maps `func` over some dimension (default: 0) of each Tensor in inputs.

vmap is useful for hiding batch dimensions: one can write a function func that runs on examples and then lift it to a function that can take batches of examples with `vmap(func)`, leading to a simpler modeling experience:


```python
import torch
from functorch import vmap
batch_size, feature_size = 3, 5
weights = torch.randn(feature_size, requires_grad=True)

def model(feature_vec):
    # Very simple linear model with activation
    assert feature_vec.dim() == 1
    return feature_vec.dot(weights).relu()

examples = torch.randn(batch_size, feature_size)
result = vmap(model)(examples)
```

When composed with `grad`, `vmap` can be used to compute per-sample-gradients:


```python
from functorch import vmap
batch_size, feature_size = 3, 5

def model(weights,feature_vec):
    # Very simple linear model with activation
    assert feature_vec.dim() == 1
    return feature_vec.dot(weights).relu()

def compute_loss(weights, example, target):
    y = model(weights, example)
    return ((y - target) ** 2).mean()  # MSELoss

weights = torch.randn(feature_size, requires_grad=True)
examples = torch.randn(batch_size, feature_size)
targets = torch.randn(batch_size)
inputs = (weights,examples, targets)
grad_weight_per_example = vmap(grad(compute_loss), in_dims=(None, 0, 0))(*inputs)
```

### vjp (vector-Jacobian product)

The `vjp` transform applies `func` to `inputs` and returns a new function that computes the vector-Jacobian product (vjp) given some `cotangents` Tensors.


```python
from functorch import vjp

inputs = torch.randn(3)
func = torch.sin
cotangents = (torch.randn(3),)

outputs, vjp_fn = vjp(func, inputs); vjps = vjp_fn(*cotangents)
```

### jvp (Jacobian-vector product)

The `jvp` transforms computes Jacobian-vector-products and is also known as "forward-mode AD". It is not a higher-order function unlike most other transforms, but it returns the outputs of `func(inputs)` as well as the jvps.


```python
from functorch import jvp
x = torch.randn(5)
y = torch.randn(5)
f = lambda x, y: (x * y)
_, output = jvp(f, (x, y), (torch.ones(5), torch.ones(5)))
assert torch.allclose(output, x + y)
```

### jacrev, jacfwd, and hessian

The `jacrev` transform returns a new function that takes in `x` and returns the Jacobian of the function
with respect to `x` using reverse-mode AD.


```python
from functorch import jacrev
x = torch.randn(5)
jacobian = jacrev(torch.sin)(x)
expected = torch.diag(torch.cos(x))
assert torch.allclose(jacobian, expected)
```

Use `jacrev` to compute the jacobian. This can be composed with `vmap` to produce batched jacobians:


```python
x = torch.randn(64, 5)
jacobian = vmap(jacrev(torch.sin))(x)
assert jacobian.shape == (64, 5, 5)
```

`jacfwd` is a drop-in replacement for `jacrev` that computes Jacobians using forward-mode AD:


```python
from functorch import jacfwd
x = torch.randn(5)
jacobian = jacfwd(torch.sin)(x)
expected = torch.diag(torch.cos(x))
assert torch.allclose(jacobian, expected)
```

Composing `jacrev` with itself or `jacfwd` can produce hessians:


```python
def f(x):
  return x.sin().sum()

x = torch.randn(5)
hessian0 = jacrev(jacrev(f))(x)
hessian1 = jacfwd(jacrev(f))(x)
```

The `hessian` is a convenience function that combines `jacfwd` and `jacrev`:


```python
from functorch import hessian

def f(x):
  return x.sin().sum()

x = torch.randn(5)
hess = hessian(f)(x)
```

## Conclusion

Check out our other tutorials (in the left bar) for more detailed explanations of how to apply functorch transforms for various use cases. `functorch` is very much a work in progress and we'd love to hear how you're using it -- we encourage you to start a conversation at our [issues tracker](https://github.com/pytorch/functorch) to discuss your use case.
