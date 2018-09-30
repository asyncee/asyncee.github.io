.. title: Получение первого элемента списка в Python
.. description: Идиоматическое решение
.. slug: poluchenie-pervogo-elementa-spiska
.. date: 2016-03-13 23:00:00 UTC+03:00

Проблема нахождения первого элемента в коллекции встречается достаточно часто.

На просторах интернета встречается огромное количество разных вариантов решения, но большинство из них не-pythonic и не удовлетворяют утверждению «простое лучше сложного»:

```python
def get_first(iterable):
    if len(iterable) > 0:
        return iterable[0]
    return None

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

def get_first(iterable):
    return iterable[0] if iterable else None
```

На мой взгляд лучше использовать вот такой вариант:

```python
x = [1, 2, 3]

first = next(iter(x), None)

first_odd = next((i for i in x if i % 2), None)
```

Такой вариант записи не только хорошо читается, но ещё и достаточно компактен для записи.
