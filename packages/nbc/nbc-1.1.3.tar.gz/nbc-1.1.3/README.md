# Number Base Converter by v01d

*Converts string representation from one base to another*

## Installation
#### From PyPI (recommended)
Via pip
```cmd
$ pip install --user nbc
```
Via pipenv
```cmd
$ pipenv install nbc
```
#### From GitLab
```cmd
$ git clone https://gitlab.com/v01d-gl/number-base-converter.git
$ cd number-base-converter
$ python setup.py install --user
```


## Docs

__convert(number, to_base, from_base)__  
*number*: from_base whole number (as String) to convert  
*to_base*: New base [2; 36]  
*from_base*: Old base [2; 36] (default 10)  
*return*: to_base number as a String

Wrong *to_base*/*from_base* range raises __ValueError__  
Int *number* raises __TypeError__  
Unexpected symbols in *number* raise __ValueError__


## Example
```python
from nbc import convert


convert('15', 2)  # '1111'
convert('10F', to_base=8, from_base=16)  # '417'
convert('1', 30)  # '1'
```
