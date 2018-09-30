.. title: Шаблон для прототипирования компонентов на reactjs в браузере
.. description: Создаём прототип компонента за несколько минут
.. slug: shablon-dlya-prototipirovaniya-komponentov-na-reactjs-v-brauzere
.. date: 2016-04-12 23:00:00 UTC+03:00


Недавно мне потребовалось очень быстро получить работающий прототип компонента на **react**, а под рукой не оказалось стандартных инструментов для создания проекта. Поэтому я немного подумал — и создал шаблон для написания компонентов прямо в браузере.

Плюс данного решения — можно уже через минуту после клонирования проекта с шаблоном получить рабочий компонент, поддерживается **ES6**, **ES7**, **JSX**.

Минусов больше — решение нестандартное, официально не поддерживается, грузится долго (загрузка библиотек, транспайлинг). Но все эти нюансы не имеют никакого значения, если вам просто нужно получить рабочий прототип — посмотреть, проверить и переписать всё нормально.

Актуальную версию исходников можно получить [по ссылке](https://github.com/asyncee/react-minimal.git).

Сам код простой:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Minimal React</title>

    <link rel="stylesheet" type="text/css" href="style.css">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.4.4/babel.min.js"></script>
    <script src="https://code.jquery.com/jquery-2.2.3.min.js"></script>
    <script src="https://fb.me/react-15.0.1.min.js"></script>
    <script src="https://fb.me/react-dom-15.0.1.min.js"></script>

    <script>
        $(function(){
            eval(Babel.transform($('script[type="text/babel"]').text(), {
                presets: ['es2015', 'react', 'stage-0']
            }).code)
        })
    </script>
</head>
<body>
    <div id="app"></div>

    <script type="text/babel">
        class HelloWorld extends React.Component {
            state = {
                greeting: 'Hello world!'
            }

            render() {
                return (
                    <div className="greeting">{this.state.greeting}</div>
                )
            }
        }
    </script>

    <script type="text/babel">
        ReactDOM.render(<HelloWorld/>, document.getElementById('app'))
    </script>

</body>
</html>
```

Как видно, для работы компонентов необходимо код размещать внутри тегов ``script`` с атрибутом ``type="text/babel"``. Содержимое тегов конкатенируется, преобразуется в ES5 и исполняется.

Вот так всё просто.
