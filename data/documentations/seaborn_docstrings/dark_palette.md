```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
Define a sequential ramp from a dark gray to a specified color:

```python
sns.dark_palette("seagreen")
```
Specify the color with a hex code:

```python
sns.dark_palette("#79C")
```
Specify the color from the husl system:

```python
sns.dark_palette((20, 60, 50), input="husl")
```
Increase the number of colors:

```python
sns.dark_palette("xkcd:golden", 8)
```
Return a continuous colormap rather than a discrete palette:

```python
sns.dark_palette("#b285bc", as_cmap=True)
```


```python

```
