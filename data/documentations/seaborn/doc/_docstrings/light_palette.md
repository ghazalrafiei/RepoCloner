```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Define a sequential ramp from a light gray to a specified color:

```python
sns.light_palette("seagreen")
```
Specify the color with a hex code:

```python
sns.light_palette("#79C")
```
Specify the color from the husl system:

```python
sns.light_palette((20, 60, 50), input="husl")
```
Increase the number of colors:

```python
sns.light_palette("xkcd:copper", 8)
```
Return a continuous colormap rather than a discrete palette:

```python
sns.light_palette("#a275ac", as_cmap=True)
```


```python

```
