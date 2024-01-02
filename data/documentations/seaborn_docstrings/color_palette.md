```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Calling with no arguments returns all colors from the current default
color cycle:

```python
sns.color_palette()
```
Other variants on the seaborn categorical color palette can be referenced by name:

```python
sns.color_palette("pastel")
```
Return a specified number of evenly spaced hues in the "HUSL" system:

```python
sns.color_palette("husl", 9)
```
Return all unique colors in a categorical Color Brewer palette:

```python
sns.color_palette("Set2")
```
Return a diverging Color Brewer palette as a continuous colormap:

```python
sns.color_palette("Spectral", as_cmap=True)
```
Return one of the perceptually-uniform palettes included in seaborn as a discrete palette:

```python
sns.color_palette("flare")
```
Return one of the perceptually-uniform palettes included in seaborn as a continuous colormap:

```python
sns.color_palette("flare", as_cmap=True)
```
Return a customized cubehelix color palette:

```python
sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
```
Return a light sequential gradient:

```python
sns.color_palette("light:#5A9", as_cmap=True)
```
Return a reversed dark sequential gradient:

```python
sns.color_palette("dark:#5A9_r", as_cmap=True)
```
Return a blend gradient between two endpoints:

```python
sns.color_palette("blend:#7AB,#EDA", as_cmap=True)
```
Use as a context manager to change the default qualitative color palette:

```python
x, y = list(range(10)), [0] * 10
hue = list(map(str, x))
```


```python
with sns.color_palette("Set3"):
    sns.relplot(x=x, y=y, hue=hue, s=500, legend=False, height=1.3, aspect=4)

sns.relplot(x=x, y=y, hue=hue, s=500, legend=False, height=1.3, aspect=4)
```
See the underlying color values as hex codes:

```python
print(sns.color_palette("pastel6").as_hex())
```


```python

```
