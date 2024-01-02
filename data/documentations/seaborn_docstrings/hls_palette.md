```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
By default, return 6 colors with identical lightness and saturation and evenly-sampled hues:

```python
sns.hls_palette()
```
Increase the number of colors:

```python
sns.hls_palette(8)
```
Decrease the lightness:

```python
sns.hls_palette(l=.3)
```
Decrease the saturation:

```python
sns.hls_palette(s=.3)
```
Change the start-point for hue sampling:

```python
sns.hls_palette(h=.5)
```
Return a continuous colormap. Notice the perceptual discontinuities, especially around yellow, cyan, and magenta: 

```python
sns.hls_palette(as_cmap=True)
```


```python

```
