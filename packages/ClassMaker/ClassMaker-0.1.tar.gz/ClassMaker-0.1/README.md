A helper class to programaticly build a Meta Class

### Install

```
git clone https://gitlab.com/craigukaea/class-maker.git
cd class-builder
./Install
```

### Use

To build a class equivelent to the following:
```python
class Foo:
    def bar():
        print("Hello world")
```

Use:
```
maker = ClassMaker()
maker.setClassName('Foo')
maker.addFunction('bar', lambda : print("Hello World!"))

#make the class
foo = maker.makeClass()

##test the functions
foo.__init__()
foo.bar()
    
```


### Example
```python
from ClassMaker import ClassMaker
    
if __name__ == "__main__":

    maker = ClassMaker()
    maker.setClassName('Foo')
    maker.addFunction('bar', lambda : print("Hello World!"))
    maker.addVariable('baz', 5)
    
    maker.addFunctionToInitialiser(lambda : print("Initialising"))
    maker.addFunctionToInitialiser(lambda : print("!"))

    foo = maker.makeClass()
    foo.__init__()
    foo.bar()
    print(foo.baz)
```
