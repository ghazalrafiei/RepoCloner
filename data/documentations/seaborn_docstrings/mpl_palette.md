```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```

Return discrete samples from a continuous matplotlib colormap:


```python
sns.mpl_palette("viridis")
```
Return the continuous colormap instead; note how the extreme values are more intense:

```python
sns.mpl_palette("viridis", as_cmap=True)
```
Return more colors:

```python
sns.mpl_palette("viridis", 8)
```
Return values from a qualitative colormap:

```python
sns.mpl_palette("Set2")
```
Notice how the palette will only contain distinct colors and can be shorter than requested:

```python
sns.mpl_palette("Set2", 10)
```


```python

```
