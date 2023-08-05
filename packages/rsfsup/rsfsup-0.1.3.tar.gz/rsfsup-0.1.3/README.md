# `rsfsup`
Python interface to the Rohde & Schwarz FSUP Signal Source Analyzer

## Installation
```linux
$ pip install rsfsup
```  

## Usage

```python
>>> from rsfsup import CommChannel
>>> with CommChannel("<ip address>") as fsup:
...     spectrum = fsup.read()
>>> import matplotlib.pyplot as plt
>>> plt.plot(*spectrum)
[<matplotlib.lines.Line2D at ...>]
>>> plt.show()
```  

## Documentation