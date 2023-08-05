# Zoetrope

This is a simple tool for creating unittest code stubs from a python file. Use it
by typing:

```python
zoetrope "relative_path/to/my/file.py"
zoetrope "pythonic.path.to.my.file"
```

The result is that zoetrope will print something like:

```python
import unittest
import a_custom_class

class TestModule(unittest.TestCase): # tests for module methods

    def test_a_function(self): # will use name of function in place of 'a_function'
        pass

    def test_2(self):
        pass

class TestClass(unittest.TestCase): # a class contained in the target module

    def test_a_function(self): # tests a class method or instance method
        pass

```

There is a hidden assumption that *your code will already run locally* - `zoetrope`
will fail if you try to generate tests for files which have ImportErrors or other
errors in them. Additionally, any relative path that uses `../` will not work.

## Future Development

1. Pytest functionality
2. Better relative path support/hacks
3. Mocks for specific calls made to external modules
