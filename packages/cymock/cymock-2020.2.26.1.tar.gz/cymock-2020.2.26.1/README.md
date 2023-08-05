# cymock

The [`unittest.mock`](https://github.com/python/cpython/blob/3.8/Lib/unittest/mock.py) standard library module (and the 
[`mock`](https://pypi.org/project/mock/) backport), tweaked to build with Cython.

## Why?

In one of my projects ([hikari](https://gitlab.com/nekokatt/hikari)), we rely on `unittest.mock` heavily, but unfortunately, the cost of
using tools such as `unittest.mock.create_autospec` is so great, that it can triple the time needed to run the test suite. 

Upon running cProfile, I found that the majority of time was taken by function calls to the aforementioned `create_autospec`, which was
not ideal.

The plan with this is to take the existing mock module and just Cythonize it. 

## How? 

A couple of changes have to be made in the source code for this to work.

### Removal of the `/` delimiter in function calls.

Python 3.8 introduces the `/` delimiter in function calls to separate positional arguments. At the time of writing, Cython does not
support this in the most recent release on PyPI.


```diff
- def foo(bar, /, baz):
+ def foo(bar, baz):
```

To remove these, we can run:

```bash
sed 's?,\s*/,?,?g' -i cymock.pyx
```

### Change `patch` to a class.

We can't monkey patch the `object` helper to the `patch` function once Cythonized as the `patch` function becomes immutable. To fix
this, we change the `patch` function to a `patch` class, and place the existing logic in the `__new__` method:

```diff
- def patch(
-         target, new=DEFAULT, spec=None, create=False,
-         spec_set=None, autospec=None, new_callable=None, **kwargs
-    ):
-        ...
+ class patch:
+    def __new__(
+         cls, target, new=DEFAULT, spec=None, create=False,
+         spec_set=None, autospec=None, new_callable=None, **kwargs
+    ):
+        ...
```

### Stub the module

So that IDEs can provide some form of autocompletion, we use MyPy's stubgen to produce the stub pyi file. This can be done by running
`make stub`.

### Cythonize the module

Cythonized sources can be produced using `make transpile`.

### Building the module and making the sdist and bdist wheel

Run `python setup.py build sdist bdist_wheel`.
