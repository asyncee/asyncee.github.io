.. title: Цепочка вызова методов в Python
.. description: Подход к реализации паттерна method chaining
.. slug: cepochka-vyzova-metodov-v-python
.. date: 2016-03-23 23:00:00 UTC+03:00

Каждый программист сталкивался с цепочками вызова методов, но не все задумываются о том, как реализуется данный паттерн. Принцип использования цепочки вызова методов заложен в API множества программных продуктов, например, **Django QuerySet**, селекторы **jQuery**, **elasticsearch-dsl Query** и так далее.

Зачем это нужно? Такой подход повышает читабельность программы. Сравните два примера:

```python
car = Car()
car.color('red')
car.mark('BMW')
car.model('M3')
```

```python
car = Car().color('red').mark('BMW').model('M3')
```

Второй пример короче и проще читается.

Цепочка вызова является реализацией [текучего интерфейса](https://ru.wikipedia.org/wiki/Fluent_interface), вся суть которого заключается в том, что в результате вызова любого метода необходимо вернуть указатель на текущий объект класса, что позволяет вызывать методы по цепочке.

Тут есть нюанс. В классической реализации методы изменяют состояние объекта, на котором вызываются, что приводит к нарушению принципа DRY и не позволяет делать такие вещи:

```python
# задача — создать две красных машины разных моделей
car = Car().color('red').mark('BMW')
m3 = car.model('m3')
m4 = car.model('m4')
```

В данном случае объект класса ``Car`` — изменяемый (mutable), а поэтому ``id(car) == id(m3) == id(m4)``, то есть это один объект.

Данное поведение не является ошибкой, когда действительно нужно изменять состояние объекта.

В противном случае, на каждом шаге необходимо возвращать **копию** объекта (необходимо учитывать повышенный расход памяти и процессорного времени). Такой подход используется в ``Django QuerySet``:

```python
active_records = Record.objects.active()  # QuerySet с базовым состоянием
new_records = active_records.new()  # Копия предыдущего QuerySet с фильтром по новым записям
old_records = active_records.old()  # Ещё одна копия QuerySet с фильтром по старым записям
```

Итак, привожу мою реализацию, с тестами. Скачать исходник вы можете из [этого gist](https://gist.github.com/asyncee/d57ad89267d16962ae75):

```python
import copy
from collections import namedtuple, Sequence


Item = namedtuple('Item', 'name, price')

items = [
    Item('apple', 10.0),
    Item('banana', 12.0),
    Item('orange', 8.0),
    Item('coconut', 50.0),
]


class Query(Sequence):
    def __init__(self, items):
        self.items = items

    def __getitem__(self, i):
        return self.items[i]

    def __len__(self):
        return len(self.items)

    def _clone(self):
        return copy.deepcopy(self)

    def first(self):
        q = self._clone()
        return next(iter(q), None)

    def last(self):
        q = self._clone()
        try:
            return q[-1]
        except KeyError:
            return None

    def values(self, attr):
        q = self._clone()
        return [getattr(o, attr) for o in q]

    def filter(self, cond):
        """
        Filter by condition.
        Condition must be a function taking one argument (an object),
        and returning True or False.
        """
        q = self._clone()
        return Query([o for o in q if cond(o)])

    @property
    def total(self):
        return sum(self.values('price'))


if __name__ == "__main__":
    q = Query(items)
    q2 = Query(items)
    assert id(q.items) != id(q2.items)

    assert q.first() == items[0]
    assert q.last() == items[-1]

    assert q.values('name') == ['apple', 'banana', 'orange', 'coconut']
    assert q.values('price') == [10.0, 12.0, 8.0, 50.0]

    assert q.filter(lambda x: x.price > 30).values('name') == ['coconut']
    assert q.filter(lambda x: x.price > 30).total == 50.0

    assert q.total == 80.0
```

Данный пример является лишь демонстрацией и говорит сам за себя. Следует учитывать, что при вызове каждого метода, происходит копирование объекта вместе со всем набором данных. Для данного конкретного случая этот момент можно оптимизировать, но уже в рамках другой статьи :)

Удачного кодинга!
