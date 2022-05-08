# Closures

```python
def make_adder(x):
    def sub(y):
        return x + y
    return sub

plus_five = make_adder(5)
print(plus_five(10))

```
