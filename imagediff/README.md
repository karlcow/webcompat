# Image Diff for Screenshots

1. Given a directory of images: `dir_path`
2. Images have the name `somename-AFTER.png` `somename-BEFORE.png`
3. For each couple of images, compute the difference.

``` python
def diff_ratio(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    return s.quick_ratio()
```
