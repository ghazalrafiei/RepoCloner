## Atlas data extraction and analysis

**This notebook requires authentication with the Performance tracking Atlas cluster, and so is only usable by Mongo employees** 

This notebook demonstrates how to extract performance data stored in an Atlas cluster and perform some simple analysis.  
The data contained in the Atlas cluster is identical to what can be [extracted from Evergreen](evergreen_analysis.ipynb), but additional fields have been provided to allow for more detailed analysis.  

In the below example historical performance data of the `perf_test_evict_btree_1` wiredtiger test on the `develop` branch is accessed, and then compared against the performance of a specific patch build `61b6b843562343496418f695`.


```python
# The test and patch build to use. Change these to produce different plots.
test_name = "perf-test-medium-multi-lsm"
patch_name = "61b6b843562343496418f695"

# Login details need to be set here.
# A username and password for read-only access to the cluster can be found on the `WiredTiger Performance Testing` Wiki page 
username="username"
password="password"
```

The script connects to the Atlas cluster using the usual Python drivers


```python
from pymongo import MongoClient

client = MongoClient(f"mongodb://{username}:{password}@wtevergreenperformance0-shard-00-00.qlpxg.mongodb.net:27017,wtevergreenperformance0-shard-00-01.qlpxg.mongodb.net:27017,wtevergreenperformance0-shard-00-02.qlpxg.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-iuj3dv-shard-0&authSource=admin&retryWrites=true&w=majority")

# Get a handle for the perf metrics collection
perf_coll = client.WTPerformanceDataDB.AllPerfTests

```

And allows the user to manipulate performance data either via `MQL` queries, or direct modification via Python.  
The below example first extracts a subset of documents via `MQL`:


```python
from bson.son import SON

pipeline = [
    {"$match": {
        "config.json_info.evergreen_task_info.task_name"  : test_name,
        "config.json_info.evergreen_task_info.execution": '0',
        "git.branch.name": "develop",
    }},
    {"$sort": SON([("Timestamp", -1)])},
    {"$limit": 100}
]

all_builds = list(perf_coll.aggregate(pipeline))

```

and then uses Python to further filter and format the data


```python
def restructure_data(commits):
    """
    Restructure the provided MQL results into a better format for plotting.
    Takes in a list of documents: 
        [{
            "Timestamp": int, 
            "metrics": [
                {"name": str, "value": int}
            ]
        }]
    and returns a Dict of metrics mapped to a list of their values over time:
        {"metric_name": {time: [int], value: [int]}}
    """
    output = {}
    for commit in commits:
        ts = commit["Timestamp"]
        for metric in commit["metrics"]:
            if "value" not in metric:
                # We only want individual data points here. Metrics containing multiple data points ("values" plural) are ignored. 
                continue

            name = metric["name"]
            val = metric["value"]
            
            if name not in output.keys():
                output[name] = {"time": [], "val": []}
            
            output[name]["time"].append(ts)
            output[name]["val"].append(val)

    return output


mainline_builds = [commit for commit in all_builds if commit["config"]["json_info"]["evergreen_task_info"]["is_patch"] == '']
patch_builds = [commit for commit in all_builds if 
    commit["config"]["json_info"]["evergreen_task_info"]["is_patch"] == 'true' and
     patch_name in commit["config"]["json_info"]["evergreen_task_info"]["task_id"]]

if len(patch_builds) == 0:
    raise ValueError(f"Error: no patch builds found for id '{patch_name}'")

formatted_mainline = restructure_data(mainline_builds)
formatted_patch = restructure_data(patch_builds)
```

Finally, this data is plotted via matplotlib


```python
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

# Plot historical mainline performance data.
colors = iter(cm.rainbow(np.linspace(0, 1, len(formatted_mainline))))
for (k, v) in formatted_mainline.items():
    plt.plot(v["time"], v["val"], color=next(colors), label=k, alpha=0.3)

# Plot the results of the patch build. The colours are selected to match the mainline data plotted above.
colors = iter(cm.rainbow(np.linspace(0, 1, len(formatted_patch))))
for (k, v) in formatted_patch.items():
    plt.plot(v["time"], v["val"], color=next(colors), marker="o")

# Create the plot.
plt.title(f"{patch_name}: {test_name}")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xticks(rotation = 45)

```




    (array([18964., 18965., 18966., 18967., 18968., 18969., 18970., 18971.,
            18972., 18973., 18974.]),
     [Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, '')])




    
![png](atlas_analysis_files/atlas_analysis_9_1.png)
    


print(client.database_names)
