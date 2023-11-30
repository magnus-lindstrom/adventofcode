# Question 7

If your problem demands a recursive solution, think through your solution before you start designing
it. This one took me ages and produced the monstrosity that is in the repo..

# imports...

## Non-relative imports

pytest does not work when imports are not relative (see below), but running the file
directly does work.

```python
from utils import get_knot_hash_of_string
```

This is with a folder structure of

src/
src/14.py
src/utils.py

## Relative imports

pytest does work when imports are relative (see below), but running the file directly does
not work.

```python
from .utils import get_knot_hash_of_string
```

This is with a folder structure of

src/
src/14.py
src/utils.py
