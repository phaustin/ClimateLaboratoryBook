---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import numpy as np
```

```{code-cell} ipython3
nlayers=5
kvals = np.arange(nlayers,-(nlayers+1),-1,dtype=int)
kvals
```

```{code-cell} ipython3
tot_trans=0.2
log_layer_trans = np.log(tot_trans)/nlayers
trans = np.exp(log_layer_trans)
print(trans**5)
```

```{code-cell} ipython3
import pprint
pp = pprint.PrettyPrinter(indent=4)

def find_diaglen(kvals,nlayers):
    nlevels=kvals[0] + 1
    keep_len=[]
    for the_k in kvals:
        if the_k >=0:
            diaglen = nlevels - the_k
        else:
            diaglen = nlevels+the_k
        keep_len.append(diaglen)
    return keep_len

def find_element(kvals,diaglen,trans):
    nlevels=kvals[0] + 1
    element_dict={}
    for the_k,the_len in zip(kvals,diaglen):
        if the_k >= 0:
            direction = -1
            the_exp=the_k
        else:
            direction = 1
            the_exp=-(the_k+1)
        the_element=(trans**the_exp)*direction
        element_dict[the_k] = {'element':the_element,
                               'exponent':the_exp,'diaglen':the_len}
    return element_dict
            
```

```{code-cell} ipython3
diaglen = find_diaglen(kvals,nlayers)
element_dict=find_element(kvals,diaglen,trans)
pp.pprint(element_dict)
```

```{code-cell} ipython3

```
