# Python Identifier Generator Tools

Identifier generator tools often used privately in Python.

Includes the following features:
- base32
  - support alphabet RFC4648, base32hex, crockford, zbase32
- base58
  - support alphabet bitcoin, ripple, flickr
  - base58check encoding
- xid
  - python implementation of xid
- uuid58
  - convert uuid to base58, base58 to uuid
  - convert uuid to base58check, base58check to uuid

## Install

Install and update using pip:
```shell
pip install -U hisak-idtools
```


## Xid Example

```python
from hisak.idtools.xid import new_xid

print(new_xid())
```


## UUID58 Example

```python
from hisak.idtools.uuid58 import uuid4

print(uuid4().base58)
```


## Links

I used the following code as reference:
- https://github.com/rs/xid
- https://github.com/graham/python_xid
- https://github.com/keis/base58
