# lis

> life's short, avoid stupid duplicate coding.

`lis` a python library including vairous state-of-art tools, enjoy!

## Install

```
pip install lis
```

## Import

```
# import all
import lis

# import specific module or function
from lis.decorators import safe_or
```


## API Reference

#### Decorators

##### lis.decorators.safe_or

##### lis.decorators.timeit

#### Collections

##### lis.collections.objectize

> lis.collections.objectize(data, recursive=True)

Convert a dictionary to object, and access the keys via attributes.

Parameters:
- data: _dict_
    Input dictionary
- recursive: _bool, optional_
    convert the data recursively if this is set as True.

#### streaming

##### lis.streaming.streaming



## Tests

```
python -m pytest tests -s
```

## Contribution

