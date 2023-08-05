

# A web crawler for academic resources


## Installation

```shell script
pip install tortoise
```

## Features

### web of science

**usage**

```python
from tortoise.scholar import AppWebKnowledge

title = 'The ERA-Interim reanalysis: configuration and performance of the data assimilation system'
apk = AppWebKnowledge(headless=False)
apk.fetch_homepage(argument=title, mode='title')
apk.parse_article()

print(apk.parsed_info)
```


### pdf bulk downloader

### baidu scholar
