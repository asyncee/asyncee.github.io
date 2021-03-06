.. title: Django 1.9 и робокасса
.. description: Как решить проблемы с тестовыми платежами
.. slug: django-19-i-robokassa
.. date: 2016-03-02 23:00:00 UTC+03:00

Возникла недавно задача реализовать возможность проведения онлайн-платежей через [робокассу](https://www.robokassa.ru). Вот уже несколько лет использую для этого приложение [django-robokassa](https://github.com/kmike/django-robokassa) от kmike.

Приложение подключил, проект настроил, соответствующий код для обработки заказов и платежей написал. Проверяю — не работает, вместо формы тестового платежа, робокасса показывает страницу с предложением зарегистрироваться и описанием сервиса. Хм.

Начал разбираться — полез в документацию сервиса и обнаружил там ссылку на проверку платежа прямо из личного кабинета. Ссылка перехода на форму тестового платежа теперь выглядит идентично форме проведения настоящих платежей и
располагается по-другому адресу: https://auth.robokassa.ru/Merchant/Index.aspx

Ко всему прочему, теперь ещё и необходимо указывать дополнительный параметр ``IsTest=1`` при отправке тестового запроса на проведение платежа, иначе платёж считается боевым.

Вариантов решения проблемы я нашёл три:

- создать issue на github автора приложения
- сделать форк приложения, исправить проблемы и сделать pull-request
- сделать форк приложения с новым именем, например, django-robokassa-asyncee и вести самостоятельную разработку (нужно проверить лицензию)

Для начала я решил выбрать первый вариант, фиксы там буквально в две строки, поэтому, если kmike заинтересован в судьбе проекта, то нужные изменения он внесёт. А в текущем проекте я просто отнаследовался от ``RobokassaForm`` и переопределил несколько методов, но это временное решение.

```python
class CustomRobokassaForm(RobokassaForm):

    @property
    def target(self):
        if conf.TEST_MODE:
            return u'https://auth.robokassa.ru/Merchant/Index.aspx'

        return conf.FORM_TARGET

    def get_redirect_url(self):
        """ Получить URL с GET-параметрами, соответствующими значениям полей в
        форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
        ручной отправке формы методом GET.
        """
        def _initial(name, field):
            val = self.initial.get(name, field.initial)
            if not val:
                return val
            return unicode(val).encode('1251')

        fields = [(name, _initial(name, field))
                  for name, field in self.fields.items()
                  if _initial(name, field)
                  ]

        if conf.TEST_MODE:
            fields.append((u'IsTest'.encode('1251'), u'1'.encode('1251')))
        params = urlencode(fields)
        return self.target+'?'+params
```

На данный момент репозиторий проекта выглядит заброшенным, возможно автор потерял интерес к приложению, такое бывает. Ничего страшного в этом нет, ведь в этом и суть OpenSource - в любой момент можно сделать свой вклад.

Кстати, недавно появился ещё один проект [django-robokassa-merchant](https://github.com/DirectlineDev/django-robokassa-merchant), основанный на оригинальном ``django-robokassa``. На данный момент проект находится в состоянии разработки, нет документации, везде пестрят надписи «TODO»,  но есть тесты, и, судя по коду, проект более перспективный, так как предполагает возможность проведения платежей из-под разных мерчантов (аккаунтов в робокассе) в рамках одного сайта, плюс используется ``GenericForeignKey`` для связи с кастомными вариантами вашей модели заказа.

**UPDATE**: автор действительно больше не поддерживает приложение, в том числе и репозиторий на bitbucket. Однако, похоже, что кто-то ранее столкнулся с такой же проблемой и решил это в своём проекте и сделал pull-request как ответ на мой issue. Изменения и merge можно посмотреть [здесь](https://github.com/kmike/django-robokassa/commit/9854d677de050e3056e7e0534c11597ca8f83f14).

На данный момент версия приложения django-robokassa в актуальном состоянии.

**UPDATE  от 30 апреля**: Пользователь Salavat Sharapov в комментариях уточнил, что есть форк на bitbucket с фиксами от Sergey Gornostayev. Посмотреть можно [здесь](https://bitbucket.org/TheDeadOne/django-robokassa/src). Из основных изменений можно выделить поддержку Python 3.5 и Django 1.9.
