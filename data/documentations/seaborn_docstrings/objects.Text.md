```python
import seaborn.objects as so
from seaborn import load_dataset
glue = (
    load_dataset("glue")
    .pivot(index=["Model", "Encoder"], columns="Task", values="Score")
    .assign(Average=lambda x: x.mean(axis=1).round(1))
    .sort_values("Average", ascending=False)
)
```
Add text at x/y locations on the plot:

```python
(
    so.Plot(glue, x="SST-2", y="MRPC", text="Model")
    .add(so.Text())
)
```
Add bar annotations, horizontally-aligned with `halign`:

```python
(
    so.Plot(glue, x="Average", y="Model", text="Average")
    .add(so.Bar())
    .add(so.Text(color="w", halign="right"))
)
```
Fine-tune the alignment using `offset`:

```python
(
    so.Plot(glue, x="Average", y="Model", text="Average")
    .add(so.Bar())
    .add(so.Text(color="w", halign="right", offset=6))
)
```
Add text above dots, mapping the text color with a third variable:

```python
(
    so.Plot(glue, x="SST-2", y="MRPC", color="Encoder", text="Model")
    .add(so.Dot())
    .add(so.Text(valign="bottom"))

)
```
Map the text alignment for better use of space:

```python
(
    so.Plot(glue, x="RTE", y="MRPC", color="Encoder", text="Model")
    .add(so.Dot())
    .add(so.Text(), halign="Encoder")
    .scale(halign={"LSTM": "left", "Transformer": "right"})
)
```
Use additional matplotlib parameters to control the appearance of the text:

```python
(
    so.Plot(glue, x="RTE", y="MRPC", color="Encoder", text="Model")
    .add(so.Dot())
    .add(so.Text({"fontweight": "bold"}), halign="Encoder")
    .scale(halign={"LSTM": "left", "Transformer": "right"})
)
```


```python

```
