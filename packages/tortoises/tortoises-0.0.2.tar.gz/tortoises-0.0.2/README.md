

# A web crawler for academic resources


## Installation

```shell script
pip install tortoises
```

## Features

### web of science

**usage**

* step 1 (install google chrome and chrome driver)

```shell script

```
* step 2 (demo) 

```python
from tortoises.scholar import AppWebKnowledge

title = 'The ERA-Interim reanalysis: configuration and performance of the data assimilation system'
apk = AppWebKnowledge(headless=True)
apk.fetch_homepage(argument=title, mode='title')
apk.parse_article()
print(apk.parsed_info)
```

### pdf bulk downloader

### scholar 



