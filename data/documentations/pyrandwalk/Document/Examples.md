| Google Colab | GitHub |
| :---: | :---: |
| <a target="_blank" href="https://colab.research.google.com/github/sadrasabouri/pyrandwalk/blob/master/Document/Examples.ipynb"><img src="https://i.ibb.co/2P3SLwK/colab.png"  style="padding-bottom:5px;" height="50px" weight="50px" /><br>Run in Google Colab</a> | <a target="_blank" href="https://github.com/sadrasabouri/pyrandwalk/blob/master/Document/Examples.ipynb"><img src="https://i.ibb.co/xfJbPmL/github.png"  height="50px" weight="50px" style="padding-bottom:5px;"/><br>View Source on GitHub</a> |

# Pyrandwalk Examples

### Version : 1.1
-----

This example set contains bellow examples from the first reference (Introduction to Stochastic Processes):
<ul>
    <ol>
        <li><a href="#Finite_Markov_Chains">Finite_Markov_Chains</a></li>
        <ul>
            <li><a href="#Exercise1_2">#Exercise1_2</a></li>
            <li><a href="#Exercise1_3">#Exercise1_3</a></li>
            <li><a href="#Exercise1_4">#Exercise1_4</a></li>
            <li><a href="#Exercise1_5">#Exercise1_5</a></li>
            <li><a href="#Exercise1_8">#Exercise1_8</a></li>
        </ul>
        <li><a href="#">Countable_Markov_Chains</a></li>
        <li><a href="#">Continous_Time_Markov_Chains</a></li>
        <li><a href="#Optimal_Stopping">Optimal_Stopping</a></li>
        <ul>
            <li><a href="#Exercise4_1">#Exercise4_1</a></li>
        </ul>
    </ol>
</ul>


```python
!pip -q -q install pyrandwalk
from pyrandwalk import *
import numpy as np
```

    /usr/lib/python3/dist-packages/secretstorage/dhcrypto.py:15: CryptographyDeprecationWarning: int_from_bytes is deprecated, use int.from_bytes instead
      from cryptography.utils import int_from_bytes
    /usr/lib/python3/dist-packages/secretstorage/util.py:19: CryptographyDeprecationWarning: int_from_bytes is deprecated, use int.from_bytes instead
      from cryptography.utils import int_from_bytes


## 1. Finite_Markov_Chains

### Exercise1_2

Consider a Markov chain with state space \{0, 1\} and transition matrix

$$
P =
\left(\begin{array}{cc} 
1/3 & 2/3\\
3/4 & 1/4
\end{array}\right)
$$


```python
states = [0, 1]
trans = np.array([[1/3, 2/3],
                  [3/4, 1/4]])
rw = RandomWalk(states, trans)
```

Assuming that the chain starts in state 0 at time n = 0, what is the probability that it is in state 1 at time n = 3?


```python
third_step_trans = rw.trans_power(3)
print(third_step_trans)
print("ANSWER:", third_step_trans[0, 1])
```

    [[0.49537037 0.50462963]
     [0.56770833 0.43229167]]
    ANSWER: 0.5046296296296295


### Exercise1_3

Consider a Markov chain with state space \{1, 2, 3\} and transition matrix

$$
P =
\left(\begin{array}{cc} 
0.4 & 0.2 & 0.4\\
0.6 & 0 & 0.4 \\
0.2 & 0.5 & 0.3
\end{array}\right)
$$



```python
states = [1, 2, 3]
trans = np.array([[0.4, 0.2, 0.4],
                  [0.6,  0 , 0.4],
                  [0.2, 0.5, 0.3]])
rw = RandomWalk(states, trans)
```

what is the probability in the long run that the chain is in state 1?
Solve this problem two different ways:

1) by raising the matrix to a high power:


```python
rw.trans_power(1000)
```




    array([[0.37878788, 0.25757576, 0.36363636],
           [0.37878788, 0.25757576, 0.36363636],
           [0.37878788, 0.25757576, 0.36363636]])



2) by directly computing the invariant probability vector as a left eigenvector:


```python
rw.final_dist()
```




    array([0.37878788, 0.25757576, 0.36363636])



### Exercise1_4

Do the same with

$$
P =
\left(\begin{array}{cc} 
0.2 & 0.4 & 0.4\\
0.1 & 0.5 & 0.4 \\
0.6 & 0.3 & 0.1
\end{array}\right)
$$



```python
states = [1, 2, 3]
trans = np.array([[0.2, 0.4, 0.4],
                  [0.1, 0.5, 0.4],
                  [0.6, 0.3, 0.1]])
rw = RandomWalk(states, trans)
```

1) by raising the matrix to a high power:


```python
rw.trans_power(1000)
```




    array([[0.28205128, 0.41025641, 0.30769231],
           [0.28205128, 0.41025641, 0.30769231],
           [0.28205128, 0.41025641, 0.30769231]])



2) by directly computing the invariant probability vector as a left eigenvector:


```python
rw.final_dist()
```




    array([0.28205128, 0.41025641, 0.30769231])



### Exercise1_5

Consider the Markov chain with state space $ S = \{0, ..., 5\} $ and transition matrix:

$$
P =
\left(\begin{array}{cc} 
0.5 & 0.5 & 0 & 0 & 0 & 0\\
0.3 & 0.7 & 0 & 0 & 0 & 0 \\
0 & 0 & 0.1 & 0 & 0 & 0.9 \\
0.25 & 0.25 & 0 & 0 & 0.25 & 0.25 \\
0 & 0 & 0.7 & 0 & 0.3 & 0 \\
0 & 0.2 & 0 & 0.2 & 0.2 & 0.4 \\
\end{array}\right)
$$



```python
states = list(range(6))
trans = np.array([[0.5, 0.5, 0  , 0  , 0  , 0  ],
                  [0.3, 0.7, 0  , 0  , 0  , 0  ],
                  [0  , 0  , 0.1, 0  , 0  , 0.9],
                  [.25, .25, 0  , 0  , .25, .25],
                  [0  , 0  , 0.7, 0  , 0.3, 0  ],
                  [0  , 0.2, 0  , 0.2, 0.2, 0.4]])
rw = RandomWalk(states, trans)
```

What are the communication classes? Which ones are recurrent and which are transient?


```python
rw.get_typeof_classes()
```




    {'recurrent': ([0, 1],
      array([[0.5, 0.5],
             [0.3, 0.7]])),
     'transient': ([2, 3, 4, 5],
      array([[0.1 , 0.  , 0.  , 0.9 ],
             [0.  , 0.  , 0.25, 0.25],
             [0.7 , 0.  , 0.3 , 0.  ],
             [0.  , 0.2 , 0.2 , 0.4 ]]))}



Suppose the system starts in state 0. What is the probability that it will be in state 0 at some large time? Answer the same question assuming the system starts in state 5.


```python
p_1000 = rw.trans_power(1000)
print(p_1000[0, 0])
print(p_1000[5, 5])
```

    0.37499999999998634
    8.081964030507363e-71


### Exercise1_8

Consider simple random walk on the graph below. (Recall that simple random walk on a graph is the Markov chain which at each time moves to an adjacent vertex, each adjacent vertex having the same probability):

$$
P =
\left(\begin{array}{cc} 
0 & 1/3 & 1/3 & 1/3 & 0 \\
1/3 & 0 & 1/3 & 0 & 1/3 \\
1/2 & 1/2 & 0 & 0 & 0 \\
1/2 & 0 & 0 & 0 & 1/2 \\
0 & 1/2 & 0 & 1/2 & 0 \\
\end{array}\right)
$$



```python
states = list(range(5))
trans = np.array([[0, 1/3, 1/3, 1/3,   0],
                  [1/3, 0, 1/3,   0, 1/3],
                  [1/2, 1/2, 0,   0,   0],
                  [1/2,   0, 0,   0, 1/2],
                  [0  , 1/2, 0, 1/2,   0]])
rw = RandomWalk(states, trans)
```

a) In the long run, what function of time is spent in vertex A?


```python
final_dist = rw.final_dist()
print(final_dist[0])
```

    0.2500000000000003


## 4. Optimal_Stopping

### Exercise4_1
Consider a simple random walk ($p = 1/2$) with absorbing boundaries on $\{0,1,2,...,10\}$. Suppose the fallowing payoff function is given:

$$
[0,2,4,3,10,0,6,4,3,3,0]
$$
Find the optimal stopping rule and give the expected payoff starting at each site.



```python
states = list(range(11))
trans = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [.5,0,.5, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, .5,0,.5, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, .5,0,.5, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, .5,0,.5, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, .5,0,.5, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, .5,0,.5, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, .5,0,.5, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, .5,0,.5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, .5,0,.5],
                  [0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 1]])
rw = RandomWalk(states, trans, payoff=[0,2,4,3,10,0,6,4,3,3,0])
```


```python
best_policy = rw.best_policy()
print(best_policy)
```

    {'continue': [1, 2, 3, 5, 6, 7, 8], 'stop': [0, 4, 9, 10]}


Which implies that it's better to stop in $[0, 4, 9, 10]$ and continue otherwise.
