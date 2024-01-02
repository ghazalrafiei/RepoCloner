```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Pass a list of two colors to interpolate between them:

```python
sns.blend_palette(["b", "r"])
```
The color list can be arbitrarily long, and any color format can be used:

```python
sns.blend_palette(["#45a872", ".8", "xkcd:golden"])
```
Return a continuous colormap instead of a discrete palette:

```python
sns.blend_palette(["#bdc", "#7b9", "#47a"], as_cmap=True)
```


```python

```
