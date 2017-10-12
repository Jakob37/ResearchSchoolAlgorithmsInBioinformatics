# Basics

* Rank: How many axes
* Array class: `ndarray` or alias `array`
    * `ndarray.ndim` - Number of axes (dimensions) of array (also called rank)
    * `ndarray.shape` - Size of each dimension of the array
    * `ndarray.size` - Number of elements in array
    * `ndarray.dtype` - Type of elements in array
    * `ndarray.itemsize` - Byte size for each element in array
    * `ndarray.data` - Buffer with actual elements, but usually accessed through indexing

# Basic example

```
import numpy as np
a = np.arange(15).reshape(3,5)  # 15 elements, organized in 3 rows and 5 cols
a.shape  # Number of elements in each dimension: (3, 5)
a.ndim   # Number of dimensions: 2
a.dtype.name  # 'int64'
a.itemsize    # 8 (bytes)
a.size        # 15 (elements)
```

# Creating arrays

```
import numpy as np

```



















