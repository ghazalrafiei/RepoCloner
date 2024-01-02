```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Return a discrete palette with default parameters:

```python
sns.cubehelix_palette()
```
Increase the number of colors:

```python
sns.cubehelix_palette(8)
```
Return a continuous colormap rather than a discrete palette:

```python
sns.cubehelix_palette(as_cmap=True)
```
Change the starting point of the helix:

```python
sns.cubehelix_palette(start=2)
```
Change the amount of rotation in the helix:

```python
sns.cubehelix_palette(rot=.2)
```
Rotate in the reverse direction:

```python
sns.cubehelix_palette(rot=-.2)
```
Apply a nonlinearity to the luminance ramp:

```python
sns.cubehelix_palette(gamma=.5)
```
Increase the saturation of the colors:

```python
sns.cubehelix_palette(hue=1)
```
Change the luminance at the start and end points:

```python
sns.cubehelix_palette(dark=.25, light=.75)
```
Reverse the direction of the luminance ramp:

```python
sns.cubehelix_palette(reverse=True)
```


```python

```
