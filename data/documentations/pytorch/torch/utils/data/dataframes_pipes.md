## \[RFC\] How DataFrames (DF) and DataPipes (DP) work together


```python
from importlib import reload
import torch
reload(torch)
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

def get_dataframes_pipe(range = 10, dataframe_size = 7):
    return ExampleIterPipe(range = range).map(lambda i: (i, i % 3))._to_dataframes_pipe(columns = ['i','j'], dataframe_size = dataframe_size)

def get_regular_pipe(range = 10):
    return ExampleIterPipe(range = range).map(lambda i: (i, i % 3))

```

Doesn't matter how DF composed internally, iterator over DF Pipe gives single rows to user. This is similar to regular DataPipe.


```python
print('DataFrames Pipe')
dp = get_dataframes_pipe()
for i in dp:
    print(i)

print('Regular DataPipe')
dp = get_regular_pipe()
for i in dp:
    print(i)
```

    DataFrames Pipe
    (0, 0)
    (1, 1)
    (2, 2)
    (3, 0)
    (4, 1)
    (5, 2)
    (6, 0)
    (7, 1)
    (8, 2)
    (9, 0)
    Regular DataPipe
    (0, 0)
    (1, 1)
    (2, 2)
    (3, 0)
    (4, 1)
    (5, 2)
    (6, 0)
    (7, 1)
    (8, 2)
    (9, 0)


You can iterate over raw DF using `raw_iterator`


```python
dp = get_dataframes_pipe()
for i in dp.raw_iterator():
    print(i)
```

       i  j
    0  0  0
    1  1  1
    2  2  2
    3  3  0
    4  4  1
    5  5  2
    6  6  0
       i  j
    0  7  1
    1  8  2
    2  9  0


Operations over DF Pipe is captured


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp['y'] = dp.i * 100 + dp.j - 2.7
print(dp.ops_str())

```

    var_3 = input_var_2.i * 100
    var_4 = var_3 + input_var_2.j
    var_5 = var_4 - 2.7
    input_var_2["y"] = var_5


Captured operations executed on `__next__` calls of constructed DataPipe


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp['y'] = dp.i * 100 + dp.j - 2.7
for i in dp.raw_iterator():
    print(i)
```

       i  j      y
    0  0  0   -2.7
    1  1  1   98.3
    2  2  2  199.3
       i  j      y
    0  3  0  297.3
    1  4  1  398.3
    2  5  2  499.3
       i  j      y
    0  6  0  597.3
    1  7  1  698.3
    2  8  2  799.3
       i  j      y
    0  9  0  897.3


`shuffle` of DataFramePipe effects rows in individual manner


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp = dp.shuffle()
print('Raw DataFrames iterator')
for i in dp.raw_iterator():
    print(i)

print('Regular DataFrames iterator')
for i in dp:
    print(i)


# this is similar to shuffle of regular DataPipe
dp = get_regular_pipe()
dp = dp.shuffle()
print('Regular iterator')
for i in dp:
    print(i)
```

    Raw DataFrames iterator
       i  j
    2  8  2
    2  2  2
    2  5  2
       i  j
    1  4  1
    1  1  1
    0  3  0
       i  j
    1  7  1
    0  9  0
    0  6  0
       i  j
    0  0  0
    Regular DataFrames iterator
    (1, 1)
    (5, 2)
    (8, 2)
    (9, 0)
    (7, 1)
    (6, 0)
    (3, 0)
    (4, 1)
    (0, 0)
    (2, 2)
    Regular iterator
    (5, 2)
    (6, 0)
    (0, 0)
    (9, 0)
    (3, 0)
    (1, 1)
    (2, 2)
    (8, 2)
    (4, 1)
    (7, 1)


You can continue mixing DF and DP operations


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp['y'] = dp.i * 100 + dp.j - 2.7
dp = dp.shuffle()
dp = dp - 17
dp['y'] = dp.y * 10000
for i in dp.raw_iterator():
    print(i)
```

        i   j          y
    0 -17 -17  -197000.0
    1 -13 -16  3813000.0
    0 -11 -17  5803000.0
        i   j          y
    2 -12 -15  4823000.0
    1 -10 -16  6813000.0
    1 -16 -16   813000.0
        i   j          y
    0  -8 -17  8803000.0
    2  -9 -15  7823000.0
    0 -14 -17  2803000.0
        i   j          y
    2 -15 -15  1823000.0


Batching combines everything into `list` it is possible to nest `list`s. List may have any number of DataFrames as soon as total number of rows equal to batch size.


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp = dp.shuffle()
dp = dp.batch(2)
print("Iterate over DataFrame batches")
for i,v in enumerate(dp):
    print(v)

# this is similar to batching of regular DataPipe
dp = get_regular_pipe()
dp = dp.shuffle()
dp = dp.batch(2)
print("Iterate over regular batches")
for i in dp:
    print(i)
```

    Iterate over DataFrame batches
    [(6, 0),(0, 0)]
    [(4, 1),(1, 1)]
    [(2, 2),(9, 0)]
    [(3, 0),(5, 2)]
    [(7, 1),(8, 2)]
    Iterate over regular batches
    [(1, 1),(4, 1)]
    [(2, 2),(3, 0)]
    [(6, 0),(7, 1)]
    [(8, 2),(0, 0)]
    [(5, 2),(9, 0)]


Some details about internal storage of batched DataFrames and how they are iterated


```python
dp = get_dataframes_pipe(dataframe_size = 3)
dp = dp.shuffle()
dp = dp.batch(2)
for i in dp:
    print("Type: ", type(i))
    print("As string: ", i)
    print("Iterated regularly:")
    print('-- batch start --')
    for item in i:
        print(item)
    print('-- batch end --')
    print("Iterated in inner format (for developers):")
    print('-- df batch start --')
    for item in i.raw_iterator():
        print(item)
    print('-- df batch end --')   
```

    Type:  <class 'torch.utils.data.datapipes.iter.dataframes.DataChunkDF'>
    As string:  [(0, 0),(3, 0)]
    Iterated regularly:
    -- batch start --
    (0, 0)
    (3, 0)
    -- batch end --
    Iterated in inner format (for developers):
    -- df batch start --
       i  j
    0  0  0
    0  3  0
    -- df batch end --
    Type:  <class 'torch.utils.data.datapipes.iter.dataframes.DataChunkDF'>
    As string:  [(6, 0),(1, 1)]
    Iterated regularly:
    -- batch start --
    (6, 0)
    (1, 1)
    -- batch end --
    Iterated in inner format (for developers):
    -- df batch start --
       i  j
    0  6  0
    1  1  1
    -- df batch end --
    Type:  <class 'torch.utils.data.datapipes.iter.dataframes.DataChunkDF'>
    As string:  [(9, 0),(4, 1)]
    Iterated regularly:
    -- batch start --
    (9, 0)
    (4, 1)
    -- batch end --
    Iterated in inner format (for developers):
    -- df batch start --
       i  j
    0  9  0
    1  4  1
    -- df batch end --
    Type:  <class 'torch.utils.data.datapipes.iter.dataframes.DataChunkDF'>
    As string:  [(5, 2),(2, 2)]
    Iterated regularly:
    -- batch start --
    (5, 2)
    (2, 2)
    -- batch end --
    Iterated in inner format (for developers):
    -- df batch start --
       i  j
    2  5  2
    2  2  2
    -- df batch end --
    Type:  <class 'torch.utils.data.datapipes.iter.dataframes.DataChunkDF'>
    As string:  [(8, 2),(7, 1)]
    Iterated regularly:
    -- batch start --
    (8, 2)
    (7, 1)
    -- batch end --
    Iterated in inner format (for developers):
    -- df batch start --
       i  j
    2  8  2
    1  7  1
    -- df batch end --


`concat` should work only of DF with same schema, this code should produce an error 


```python
# TODO!
# dp0 = get_dataframes_pipe(range = 8, dataframe_size = 4)
# dp = get_dataframes_pipe(range = 6, dataframe_size = 3)
# dp['y'] = dp.i * 100 + dp.j - 2.7
# dp = dp.concat(dp0)
# for i,v in enumerate(dp.raw_iterator()):
#     print(v)
```

`unbatch` of `list` with DataFrame works similarly to regular unbatch.
Note: DataFrame sizes might change


```python
dp = get_dataframes_pipe(range = 18, dataframe_size = 3)
dp['y'] = dp.i * 100 + dp.j - 2.7
dp = dp.batch(5).batch(3).batch(1).unbatch(unbatch_level = 3)

# Here is bug with unbatching which doesn't detect DF type.
dp['z'] = dp.y - 100

for i in dp.raw_iterator():
    print(i)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-12-fa80e9c68655> in <module>
          4 
          5 # Here is bug with unbatching which doesn't detect DF type.
    ----> 6 dp['z'] = dp.y - 100
          7 
          8 for i in dp.raw_iterator():


    ~/dataset/pytorch/torch/utils/data/dataset.py in __getattr__(self, attribute_name)
        222             return function
        223         else:
    --> 224             raise AttributeError
        225 
        226     def __reduce_ex__(self, *args, **kwargs):


    AttributeError: 


`map` applied to individual rows, `nesting_level` argument used to penetrate batching


```python
dp = get_dataframes_pipe(range = 10, dataframe_size = 3)
dp = dp.map(lambda x: x + 1111)
dp = dp.batch(5).map(lambda x: x * 1000, nesting_level = 1)
print("Iterate over DataFrame batches")
for i in dp:
    print(i)

# Similarly works on row level for classic DataPipe elements
dp = get_regular_pipe(range = 10)
dp = dp.map(lambda x: (x[0] + 1111, x[1]))
dp = dp.batch(5).map(lambda x: (x[0] * 1000, x[1]), nesting_level = 1)
print("Iterate over regular batches")
for i in dp:
    print(i)


```

    Iterate over DataFrame batches
    [(1111000, 1111000),(1112000, 1112000),(1113000, 1113000),(1114000, 1111000),(1115000, 1112000)]
    [(1116000, 1113000),(1117000, 1111000),(1118000, 1112000),(1119000, 1113000),(1120000, 1111000)]
    Iterate over regular batches
    [(1111000, 0),(1112000, 1),(1113000, 2),(1114000, 0),(1115000, 1)]
    [(1116000, 2),(1117000, 0),(1118000, 1),(1119000, 2),(1120000, 0)]


`filter` applied to individual rows, `nesting_level` argument used to penetrate batching


```python
dp = get_dataframes_pipe(range = 30, dataframe_size = 3)
dp = dp.filter(lambda x: x.i > 5)
dp = dp.batch(5).filter(lambda x: x.i < 13, nesting_level = 1)
print("Iterate over DataFrame batches")
for i in dp:
    print(i)

# Similarly works on row level for classic DataPipe elements
dp = get_regular_pipe(range = 30)
dp = dp.filter(lambda x: x[0] > 5)
dp = dp.batch(5).filter(lambda x: x[0] < 13, nesting_level = 1)
print("Iterate over regular batches")
for i in dp:
    print(i)
```

    Iterate over DataFrame batches
    [(6, 0),(7, 1),(8, 2),(9, 0),(10, 1)]
    [(11, 2),(12, 0)]
    Iterate over regular batches
    [(6, 0),(7, 1),(8, 2),(9, 0),(10, 1)]
    [(11, 2),(12, 0)]

