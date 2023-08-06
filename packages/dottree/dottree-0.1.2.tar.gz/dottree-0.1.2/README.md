# dottree

An "Enhanced defaultdict", I have been using this construct in my code many time ends up writing the biolerplate getter setter many times. So packed into a module to share with you all.


# How to install

- Use pip to install 
- tested in Python2


```bash 
pip install dottree 
```

# Quick check

```python 

'''
How to use:
- use like a dict
- use like an object 
- Go as deep you need

'''

from dottree import dotree as dot

d = dot()
d.M.J = 7
assert  d.M.J  == 7
assert  d['M']['J']  == 7

# downgrade to a dict any time
print dict(d.M) # {'J': 7}

```
