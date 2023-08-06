# OpenStreetMap
`openstreetmap` is a pure Python library that provides an easy way to extracting [OpenStreetMap](https://www.openstreetmap.org/) coordinates by name or relation id.


**Code example**

```python
# -*- coding: UTF-8 -*-
from openstreemap import Crawler

c = Crawler()
boundary = c.name_parse('合肥市蜀山区', level='county',coo_order=True)
# level: country state city county town
# coo_order  :False ->lng,lat ; True -> lat,lng  coo_order;
print(boundary.info)
boundary = c.id_parse("2458199", csys='wgs84', coo_order=True)
# csys(Coordinate System): wgs84 gcj02 bd09
print(boundary.info)
```

```boundary.info
{'name': '', 'relation_id': '', 'boundary': {'outer': '', 'inner': ''}}
```


### Installation
---

`openstreetmap ` is hosted on [PYPI](https://pypi.org/project/openstreetmap/) and can be installed as such:

```
$ pip install openstreetmap
```

Alternatively, you can also get the latest source code from [GitHub](https://github.com/Mywayking/openstreetmap) and install it manually:

```
$ git clone https://github.com/Mywayking/openstreetmap.git
$ cd openstreetmap
$ python setup.py install
```

For update:

```
$ pip install openstreetmap --upgrade
```


### License
---


Galen @__20180521__