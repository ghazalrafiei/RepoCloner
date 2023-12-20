# DataPipe Typing System

DataPipe typing system is introduced to make the graph of DataPipes more reliable and provide type inference for users. The typing system provide the flexibility for users to determine which level(s) to have type enforcement and risk false positive errors.


```python
from torch.utils.data import IterDataPipe
from typing import Any, Iterator, List, Tuple, TypeVar, Set, Union

T_co = TypeVar('T_co', covariant=True)
```


```python
# Hide traceback of Error
import functools
ipython = get_ipython()
def showtraceback(self, exc_tuple=None, filename=None, tb_offset=None,
                  exception_only=False, running_compiled_code=False):
    try:
        try:
            etype, value, tb = self._get_exc_info(exc_tuple)
        except ValueError:
            print('No traceback available to show.', file=sys.stderr)
            return

        # Hide traceback
        stb = self.InteractiveTB.get_exception_only(etype, value)

        self._showtraceback(etype, value, stb)

    except KeyboardInterrupt:
        print('\n' + self.get_exception_only(), file=sys.stderr)
ipython.showtraceback = functools.partial(showtraceback, ipython)
```

## Compile-time
Compile-time typing is enabled by default for now. And it will generate an attribute of `type` for each DataPipe. If there is no type hint specified, the DataPipe is set to a default type `Any`.

### Invalid Typing
- Return type hint of `__iter__` is not `Iterator`


```python
class InvalidDP1(IterDataPipe[int]):
    def __iter__(self) -> str:
        pass
```


    TypeError: Expected 'Iterator' as the return annotation for `__iter__` of InvalidDP1, but found str



- Return type hint of `__iter__` doesn't match or is subtype of the declared type hint


```python
class InvalidDP2(IterDataPipe[int]):
    def __iter__(self) -> Iterator[str]:
        pass
```


    TypeError: Expected return type of '__iter__' as a subtype of int, but found str for InvalidDP2



### Valid Typing

- It's allowed that return type is a subtype of class type annotation


```python
class DP(IterDataPipe[Tuple]):
    def __iter__(self) -> Iterator[Tuple[int, str]]:
        pass
```


```python
class DP(IterDataPipe):
    def __iter__(self) -> Iterator[int]:
        pass
```

- Default Typing (Any) with/without return hint for `__iter__`


```python
class DP(IterDataPipe):
    def __iter__(self):
        pass
print(DP.type)
class DP(IterDataPipe):
    def __iter__(self) -> Iterator:
        pass
print(DP.type)
class DP(IterDataPipe):
    def __iter__(self) -> Iterator[T_co]:
        pass
print(DP.type)
```

    typing.Any
    typing.Any
    typing.Any


- Matched type hints (including equal but not same types)


```python
class DP(IterDataPipe[Tuple[T_co, str]]):
    def __iter__(self) -> Iterator[Tuple[T_co, str]]:
        pass
print(DP.type)

T = TypeVar('T', int, str)  # equals to Union[int, str]
class DP(IterDataPipe[Tuple[T, str]]):
    def __iter__(self) -> Iterator[Tuple[Union[int, str], str]]:
        pass
print(DP.type)
```

    typing.Tuple[+T_co, str]
    typing.Tuple[~T, str]


### Attribute `type`
The attribute `type` is added into each DataPipe class.


```python
def print_helper(cls, obj):
    print("DataPipe[{}]\nInstance type: {}"
          .format(cls.type, obj.type))
```


```python
class DP(IterDataPipe[List[int]]):
    def __iter__(self) -> Iterator[List[int]]:
        pass
print_helper(DP, DP())
```

    DataPipe[typing.List[int]]
    Instance type: typing.List[int]



```python
class DP(IterDataPipe[Any]):
    def __iter__(self) -> Iterator[Any]:
        pass
print_helper(DP, DP())
```

    DataPipe[typing.Any]
    Instance type: typing.Any



```python
class DP(IterDataPipe[tuple]):
    def __iter__(self) -> Iterator[tuple]:
        pass
print_helper(DP, DP())
```

    DataPipe[tuple]
    Instance type: tuple


## Construct-time

Construct-time type checking can be enabled by a decorator `argument_validation`. Users can opt in by attaching the decorator to `__init__`function, then users can run operations with the type inference of input `DataPipe`(s).


```python
from torch.utils.data import argument_validation

class DP(IterDataPipe):
    @argument_validation
    def __init__(self, dp: IterDataPipe[Union[int, tuple]]):
        self.dp = dp

    def __iter__(self):
        for d in self.dp:
            yield d
```


```python
dp = DP(range(10))
```


    TypeError: Expected argument 'dp' as a IterDataPipe, but found <class 'range'>



- When any input is annotated by `IterDataPipe` with detail typing hints, the `type` of input instance must be a subtype of the hint.


```python
class Temp(IterDataPipe[str]):
    def __iter__(self):
        pass
dp = DP(Temp())
```


    TypeError: Expected type of argument 'dp' as a subtype of hint typing.Union[int, tuple], but found str



- Example of valid input `DataPipe`


```python
class Temp(IterDataPipe[Tuple[int, T_co]]):
    def __iter__(self):
        pass
dp = DP(Temp())
```

## Runtime


### Decorator
Runtime type checking is enabled by a decorator `runtime_validation`. Users can opt in by attaching the decorator to `__iter__` to check the output data is an instance of subtype of `type` attribute of the DataPipe.

Note: This decorator is only allowed to be attached to `__iter__` for now. It can be extended into `__getitem__` and further `nonblocking` functions.

`runtime_validation_disabled` is a context manager to turn off the type validaiton during runtime. It's useful for DataLoader to disable the runtime validaiton after the first epoch is finished for better performance. Note: the runtime validation is enabled by default.


```python
from torch.utils.data import runtime_validation, runtime_validation_disabled

class DP(IterDataPipe[Tuple[int, T_co]]):
    def __init__(self, datasource):
        self.ds = datasource
        
    @runtime_validation
    def __iter__(self):
        for d in self.ds:
            yield d
```

Raise `RuntimeError` when the data is not of subtype

- `str` is not subtype of `int`


```python
dp = DP([(1, 1), (2, 2), ('3', 3)])
for d in dp:
    print(d)
```

    (1, 1)
    (2, 2)



    RuntimeError: Expected an instance as subtype of typing.Tuple[int, +T_co], but found ('3', 3)(<class 'tuple'>)



 - Context manager to disable the runtime validation


```python
with runtime_validation_disabled():
    print(list(dp))
```

    [(1, 1), (2, 2), ('3', 3)]


- `List` is not subtype of `Tuple`


```python
dp = DP([(1, 1), (2, 2), [3, 3]])
for d in dp:
    print(d)
```

    (1, 1)
    (2, 2)



    RuntimeError: Expected an instance as subtype of typing.Tuple[int, +T_co], but found [3, 3](<class 'list'>)



- Context manager to disable the runtime validation


```python
with runtime_validation_disabled():
    print(list(dp))
```

    [(1, 1), (2, 2), [3, 3]]


- No error will be raised when all data pass the validation


```python
dp = DP([(1, 1), (2, '2'), (3, 3.)])
print(list(dp))
```

    [(1, 1), (2, '2'), (3, 3.0)]


### Reinforce type for DataPipe instance


```python
T = TypeVar('T', int, str)
ds = list(range(10))
```

- If the DataPipe class is not decorated with `runtime_validation` and the DataPipe instance calls `reinforce_type`, a warning will be raised.


```python
class DP(IterDataPipe[T]):
    def __init__(self, ds):
        self.ds = ds
        
    def __iter__(self):
        for d in self.ds:
            yield d
dp = DP(ds).reinforce_type(int)
```

    /Users/erjia/workspace/pytorch-dev/typing/torch/utils/data/_typing.py:346: UserWarning: The type of data generated from `DataPipe` instance won't be validated at runtime. Decorator of `runtime_validation` is required to be attached to `__iter__` method of <class '__main__.DP'> for runtime type validation
      warnings.warn("The type of data generated from `DataPipe` instance won't be validated "



```python
class DP(IterDataPipe[T]):
    def __init__(self, ds):
        self.ds = ds
        
    @runtime_validation
    def __iter__(self):
        for d in self.ds:
            yield d
```

- expected type must be a subtype of the original type hint


```python
dp = DP(ds).reinforce_type(float)
```


    TypeError: Expected 'expected_type' as a subtype of ~T, but found float



- Integer data is not subtype of str


```python
dp = DP(ds).reinforce_type(str)
list(dp)
```


    RuntimeError: Expected an instance as subtype of str, but found 0(<class 'int'>)



- Compatible with context mangager to disable validation


```python
with runtime_validation_disabled():
    print(list(dp))
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


- Valid type enforcement


```python
dp = DP(ds).reinforce_type(int)
print(list(dp))
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


- Different type based on the logic of class initialization


```python
class DP(IterDataPipe[Union[int, str]]):
    def __init__(self, label):
        if label == 'int':
            self.reinforce_type(int)
        elif label == 'str':
            self.reinforce_type(str)
```


```python
dp = DP('int')
print(dp.type)
```

    int



```python
dp = DP('str')
print(dp.type)
```

    str



```python
dp = DP('')
print(dp.type)
```

    typing.Union[int, str]

