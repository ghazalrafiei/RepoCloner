## Standard flow control and data processing DataPipes


```python
from torch.utils.data import IterDataPipe
```


```python
# Example IterDataPipe
class ExampleIterPipe(IterDataPipe):
    def __init__(self, range = 20):
        self.range = range
    def __iter__(self):
        for i in range(self.range):
            yield i
```

## Batch

Function: `batch`

Description: 

Alternatives:

Arguments:
  - `batch_size: int` desired batch size
  - `unbatch_level:int = 0` if specified calls `unbatch(unbatch_level=unbatch_level)` on source datapipe before batching (see `unbatch`)
  - `drop_last: bool = False`

Example:

Classic batching produce partial batches by default



```python
dp = ExampleIterPipe(10).batch(3)
for i in dp:
    print(i)
```

    [0, 1, 2]
    [3, 4, 5]
    [6, 7, 8]
    [9]


To drop incomplete batches add `drop_last` argument


```python
dp = ExampleIterPipe(10).batch(3, drop_last = True)
for i in dp:
    print(i)
```

    [0, 1, 2]
    [3, 4, 5]
    [6, 7, 8]


Sequential calling of `batch` produce nested batches


```python
dp = ExampleIterPipe(30).batch(3).batch(2)
for i in dp:
    print(i)
```

    [[0, 1, 2], [3, 4, 5]]
    [[6, 7, 8], [9, 10, 11]]
    [[12, 13, 14], [15, 16, 17]]
    [[18, 19, 20], [21, 22, 23]]
    [[24, 25, 26], [27, 28, 29]]


It is possible to unbatch source data before applying the new batching rule using `unbatch_level` argument


```python
dp = ExampleIterPipe(30).batch(3).batch(2).batch(10, unbatch_level=-1)
for i in dp:
    print(i)
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]


## Unbatch

Function: `unbatch`

Description: 

Alternatives:

Arguments:
    `unbatch_level:int = 1`
 
Example:


```python
dp = ExampleIterPipe(10).batch(3).shuffle().unbatch()
for i in dp:
    print(i)
```

    9
    0
    1
    2
    6
    7
    8
    3
    4
    5


By default unbatching is applied only on the first layer, to unbatch deeper use `unbatch_level` argument


```python
dp = ExampleIterPipe(40).batch(2).batch(4).batch(3).unbatch(unbatch_level = 2)
for i in dp:
    print(i)
```

    [0, 1]
    [2, 3]
    [4, 5]
    [6, 7]
    [8, 9]
    [10, 11]
    [12, 13]
    [14, 15]
    [16, 17]
    [18, 19]
    [20, 21]
    [22, 23]
    [24, 25]
    [26, 27]
    [28, 29]
    [30, 31]
    [32, 33]
    [34, 35]
    [36, 37]
    [38, 39]


Setting `unbatch_level` to `-1` will unbatch to the lowest level


```python
dp = ExampleIterPipe(40).batch(2).batch(4).batch(3).unbatch(unbatch_level = -1)
for i in dp:
    print(i)
```

    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
    32
    33
    34
    35
    36
    37
    38
    39


## Map

Function: `map`

Description: 

Alternatives:

Arguments:
  - `nesting_level: int = 0`
 
Example:


```python
dp = ExampleIterPipe(10).map(lambda x: x * 2)
for i in dp:
    print(i)
```

    0
    2
    4
    6
    8
    10
    12
    14
    16
    18


`map` by default applies function to every mini-batch as a whole



```python
dp = ExampleIterPipe(10).batch(3).map(lambda x: x * 2)
for i in dp:
    print(i)
```

    [0, 1, 2, 0, 1, 2]
    [3, 4, 5, 3, 4, 5]
    [6, 7, 8, 6, 7, 8]
    [9, 9]


To apply function on individual items of the mini-batch use `nesting_level` argument


```python
dp = ExampleIterPipe(10).batch(3).batch(2).map(lambda x: x * 2, nesting_level = 2)
for i in dp:
    print(i)
```

    [[0, 2, 4], [6, 8, 10]]
    [[12, 14, 16], [18]]


Setting `nesting_level` to `-1` will apply `map` function to the lowest level possible


```python
dp = ExampleIterPipe(10).batch(3).batch(2).batch(2).map(lambda x: x * 2, nesting_level = -1)
for i in dp:
    print(i)
```

    [[[0, 2, 4], [6, 8, 10]], [[12, 14, 16], [18]]]


## Filter

Function: `filter`

Description: 

Alternatives:

Arguments:
  - `nesting_level: int = 0`
  - `drop_empty_batches = True` whether empty many batches dropped or not.
 
Example:


```python
dp = ExampleIterPipe(10).filter(lambda x: x % 2 == 0)
for i in dp:
    print(i)
```

    0
    2
    4
    6
    8


Classic `filter` by default applies filter function to every mini-batches as a whole 



```python
dp = ExampleIterPipe(10)
dp = dp.batch(3).filter(lambda x: len(x) > 2)
for i in dp:
    print(i)
```

    [0, 1, 2]
    [3, 4, 5]
    [6, 7, 8]


You can apply filter function on individual elements by setting `nesting_level` argument


```python
dp = ExampleIterPipe(10)
dp = dp.batch(3).filter(lambda x: x > 4, nesting_level = 1)
for i in dp:
    print(i)
```

    [5]
    [6, 7, 8]
    [9]


If mini-batch ends with zero elements after filtering default behaviour would be to drop them from the response. You can override this behaviour using `drop_empty_batches` argument.



```python
dp = ExampleIterPipe(10)
dp = dp.batch(3).filter(lambda x: x > 4, nesting_level = -1, drop_empty_batches = False)
for i in dp:
    print(i)
```

    []
    [5]
    [6, 7, 8]
    [9]



```python
dp = ExampleIterPipe(20)
dp = dp.batch(3).batch(2).batch(2).filter(lambda x: x < 4 or x > 9 , nesting_level = -1, drop_empty_batches = False)
for i in dp:
    print(i)
```

    [[[0, 1, 2], [3]], [[], [10, 11]]]
    [[[12, 13, 14], [15, 16, 17]], [[18, 19]]]


## Shuffle

Function: `shuffle`

Description: 

Alternatives:

Arguments:
  - `unbatch_level:int = 0` if specified calls `unbatch(unbatch_level=unbatch_level)` on source datapipe before batching (see `unbatch`)
  - `buffer_size: int = 10000`
 
Example:


```python
dp = ExampleIterPipe(10).shuffle()
for i in dp:
    print(i)
```

    2
    9
    4
    0
    3
    7
    8
    5
    6
    1


`shuffle` operates on input mini-batches similar as on individual items


```python
dp = ExampleIterPipe(10).batch(3).shuffle()
for i in dp:
    print(i)
```

    [0, 1, 2]
    [3, 4, 5]
    [9]
    [6, 7, 8]


To shuffle elements across batches use `shuffle(unbatch_level)` followed by `batch` pattern 


```python
dp = ExampleIterPipe(10).batch(3).shuffle(unbatch_level = -1).batch(3)
for i in dp:
    print(i)
```

    [2, 1, 0]
    [7, 9, 6]
    [3, 5, 4]
    [8]


## Collate

Function: `collate`

Description: 

Alternatives:

Arguments:
 
Example:


```python
dp = ExampleIterPipe(10).batch(3).collate()
for i in dp:
    print(i)
```

    tensor([0, 1, 2])
    tensor([3, 4, 5])
    tensor([6, 7, 8])
    tensor([9])


## GroupBy

Function: `groupby`

Usage: `dp.groupby(lambda x: x[0])`

Description: Batching items by combining items with same key into same batch 

Arguments:
 - `group_key_fn`
 - `group_size` - yeild resulted group as soon as `group_size` elements accumulated
 - `guaranteed_group_size:int = None`
 - `unbatch_level:int = 0` if specified calls `unbatch(unbatch_level=unbatch_level)` on source datapipe before batching (see `unbatch`)

#### Attention
As datasteam can be arbitrary large, grouping is done on best effort basis and there is no guarantee that same key will never present in the different groups. You can call it local groupby where locallity is the one DataPipe process/thread.


```python
dp = ExampleIterPipe(10).shuffle().groupby(lambda x: x % 3)
for i in dp:
    print(i)
```

    [0, 3, 6, 9]
    [1, 4, 7]
    [5, 2, 8]


By default group key function is applied to entire input (mini-batch)


```python
dp = ExampleIterPipe(10).batch(3).groupby(lambda x: len(x))
for i in dp:
    print(i)
```

    [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    [[9]]


It is possible to unnest items from the mini-batches using `unbatch_level` argument


```python
dp = ExampleIterPipe(10).batch(3).groupby(lambda x: x % 3, unbatch_level = 1)
for i in dp:
    print(i)
```

    [0, 3, 6, 9]
    [1, 4, 7]
    [2, 5, 8]


When internal buffer (defined by `buffer_size`) is overfilled, groupby will yield biggest group available


```python
dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, buffer_size = 5)
for i in dp:
    print(i)
```

    [9, 3]
    [13, 4, 7]
    [2, 11, 14, 5]
    [0, 6, 12]
    [1, 10]
    [8]


`groupby` will produce `group_size` sized batches on as fast as possible basis


```python
dp = ExampleIterPipe(18).shuffle().groupby(lambda x: x % 3, group_size = 3)
for i in dp:
    print(i)
```

    [6, 3, 12]
    [1, 16, 7]
    [2, 5, 8]
    [14, 11, 17]
    [15, 9, 0]
    [10, 4, 13]


Remaining groups must be at least `guaranteed_group_size` big. 


```python
dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, group_size = 3, guaranteed_group_size = 2)
for i in dp:
    print(i)
```

    [11, 2, 5]
    [1, 4, 10]
    [0, 9, 6]
    [14, 8]
    [13, 7]
    [12, 3]


Without defined `group_size` function will try to accumulate at least `guaranteed_group_size` elements before yielding resulted group


```python
dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, guaranteed_group_size = 2)
for i in dp:
    print(i)
```

    [3, 6, 9, 12, 0]
    [14, 2, 8, 11, 5]
    [7, 4, 1, 13, 10]


This behaviour becomes noticable when data is bigger than buffer and some groups getting evicted before gathering all potential items


```python
dp = ExampleIterPipe(15).groupby(lambda x: x % 3, guaranteed_group_size = 2, buffer_size = 6)
for i in dp:
    print(i)
```

    [0, 3]
    [1, 4, 7]
    [2, 5, 8]
    [6, 9, 12]
    [10, 13]
    [11, 14]


With randomness involved you might end up with incomplete groups (so next example expected to fail in most cases)


```python
dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, guaranteed_group_size = 2, buffer_size = 6)
for i in dp:
    print(i)
```

    [14, 5, 11]
    [1, 7, 4, 10]
    [0, 12, 6]
    [8, 2]
    [9, 3]



    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-31-673b9dd7fb43> in <module>
          1 dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, guaranteed_group_size = 2, buffer_size = 6)
    ----> 2 for i in dp:
          3     print(i)


    ~/dataset/pytorch/torch/utils/data/datapipes/iter/grouping.py in __iter__(self)
        275 
        276             if self.guaranteed_group_size is not None and biggest_size < self.guaranteed_group_size and not self.drop_remaining:
    --> 277                 raise Exception('Failed to group items', str(buffer[biggest_key]))
        278 
        279             if self.guaranteed_group_size is None or biggest_size >= self.guaranteed_group_size:


    Exception: ('Failed to group items', '[13]')


To avoid this error and drop incomplete groups, use `drop_remaining` argument


```python
dp = ExampleIterPipe(15).shuffle().groupby(lambda x: x % 3, guaranteed_group_size = 2, buffer_size = 6, drop_remaining = True)
for i in dp:
    print(i)
```

    [5, 2, 14]
    [4, 7, 13, 1, 10]
    [12, 6, 3, 9]
    [8, 11]


## Zip

Function: `zip`

Description: 

Alternatives:

Arguments:
 
Example:


```python
_dp = ExampleIterPipe(5).shuffle()
dp = ExampleIterPipe(5).zip(_dp)
for i in dp:
    print(i)
```

    (0, 3)
    (1, 0)
    (2, 4)
    (3, 2)
    (4, 1)


## Fork

Function: `fork`

Description: 

Alternatives:

Arguments:
 
Example:


```python
dp = ExampleIterPipe(2)
dp1, dp2, dp3 = dp.fork(3)
for i in dp1 + dp2 + dp3:
    print(i)
```

    0
    1
    0
    1
    0
    1


## Demultiplexer

Function: `demux`

Description: 

Alternatives:

Arguments:
 
Example:


```python
dp = ExampleIterPipe(10)
dp1, dp2, dp3 = dp.demux(3, lambda x: x % 3)
for i in dp2:
    print(i)
```

    1
    4
    7


## Multiplexer

Function: `mux`

Description: 

Alternatives:

Arguments:
 
Example:


```python
dp1 = ExampleIterPipe(3)
dp2 = ExampleIterPipe(3).map(lambda x: x * 10)
dp3 = ExampleIterPipe(3).map(lambda x: x * 100)

dp = dp1.mux(dp2, dp3)
for i in dp:
    print(i)
```

    0
    0
    0
    1
    10
    100
    2
    20
    200


## Concat

Function: `concat`

Description: Returns DataPipes with elements from the first datapipe following by elements from second datapipes

Alternatives:
    
    `dp = dp.concat(dp2, dp3)`
    `dp = dp.concat(*datapipes_list)`

Example:



```python
dp = ExampleIterPipe(4)
dp2 = ExampleIterPipe(3)
dp = dp.concat(dp2)
for i in dp:
    print(i)
```

    0
    1
    2
    3
    0
    1
    2

