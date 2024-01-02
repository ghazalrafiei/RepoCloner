```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Generate diverging ramps from blue to red through white:

```python
sns.diverging_palette(240, 20)
```
Change the center color to be dark:

```python
sns.diverging_palette(240, 20, center="dark")
```
Return a continuous colormap rather than a discrete palette:

```python
sns.diverging_palette(240, 20, as_cmap=True)
```
Increase the amount of separation around the center value:

```python
sns.diverging_palette(240, 20, sep=30, as_cmap=True)
```
Use a magenta-to-green palette instead:

```python
sns.diverging_palette(280, 150)
```
Decrease the saturation of the endpoints:

```python
sns.diverging_palette(280, 150, s=50)
```
Decrease the lightness of the endpoints:

```python
sns.diverging_palette(280, 150, l=35)
```


```python

```


```python

```
