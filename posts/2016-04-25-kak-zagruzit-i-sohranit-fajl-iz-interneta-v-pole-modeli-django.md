.. title: Как сохранить файл, доступный по ссылке в поле модели Django
.. description: Как вручную скачать файл и сохранить его в FileField / ImageField
.. slug: kak-zagruzit-i-sohranit-fajl-iz-interneta-v-pole-modeli-django
.. date: 2016-04-25 23:00:00 UTC+03:00


Для решения этой задачи можно использовать разные способы, в том числе с загрузкой в оперативную память, но я предпочитаю сначала сохранить файл на жёсткий диск, а затем передать его на обработку в Django.

Код простой:

```python
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models.fields.files import FieldFile
from django.db.models import Model


def save_file_from_url(model, url, save_to=None, filename=None):
    """
    Сохранить файл, доступный по адресу ``url`` в поле ``save_to`` модели ``model``.

    Аргументы:
        model — объект класса Model, либо FieldFile / ImageFieldFile
        url — ссылка на файл
        save_to — название файлового поля
        filename — новое имя для сохраняемого файла

    Примеры использования:
        save_file_from_url(gallery, '<url>', save_to='image')
        save_file_from_url(gallery.image, '<url>')
    """
    assert isinstance(model, (FieldFile, Model)), '"model" argument should be a Model or FieldFile instance'

    if isinstance(model, FieldFile):
        field = model
    else:
        assert isinstance(save_to, str), '"save_to" argument must be provided along with Model instance'
        field = getattr(model, save_to)

    r = requests.get(url)

    if not filename:
        filename = url.split('/')[-1]

    temp_file = NamedTemporaryFile(delete=True)
    temp_file.write(r.content)
    temp_file.flush()

    field.save(filename, File(temp_file), save=True)
```

Вот ещё несколько примеров реализации:

- [django snippets](https://djangosnippets.org/snippets/2838/)
- [stackoverflow](Programmatically saving image to Django ImageField)

Единственное, что стоит учесть — в данной реализации используется библиотека ``requests``, которая не умеет открывать локальные файлы (``file:///tmp/file.txt``).
