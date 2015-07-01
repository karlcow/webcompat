# Image Diff for Screenshots

1. Given a directory of images: `dir_path`
2. Images have the name `somename-AFTER.png` `somename-BEFORE.png`
3. For each couple of images, compute the difference.

``` python
def diff_ratio(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    return s.quick_ratio()
```

[Example](https://gist.github.com/karlcow/a7e9f367c77f9dd57490) of a run with [this version](https://github.com/karlcow/webcompat/blob/4b7a784fbdbf1649d3e93e511e0fa62f5e824550/imagediff/reportimgdiff.py)

[Some notes](https://groups.google.com/forum/#!topic/mozilla.compatibility/xFk15n5MDfU) related to this experiment and more specifically 

* I should reorganize the files by putting them in separate folder according to their ratio result.
* I should test that an image is all white (aka 1.0 result but nothing on screen)
* In this case it would be good in fact to have 3 screenshots (ref, old build, new build)
* news sites are tough. Ads are making life difficult.
* screenshots are not interactions (obviously) 
