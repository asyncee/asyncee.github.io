.. title: Настройка webpack для работы с react и sass
.. description: Или вебпак для начинающих хипстеров
.. slug: nastrojka-webpack-dlya-raboty-s-react-i-scss
.. date: 2016-04-07 23:00:00 UTC+03:00

**NOTE**: *Друзья, обратите внимание, что с момента публикации прошло больше года, за это время в мире фронтенд разработки произошло большое количество изменений, поэтому данная статья потеряла свою актуальность*.

В этой статье я опишу как настроить [webpack](https://webpack.github.io/) с поддержкой замечательного фреймворка [react](https://facebook.github.io/react/) для определения структуры интерфейса и [sass](http://sass-lang.com/) для его стилизации.

На самом деле эти технологии можно использовать и без webpack, например, встраивать напрямую в код веб-страницы, но с бандлером это делать не только удобнее, но и решение получается более производительным.

Сразу оговорюсь, что я всё-таки больше backend developer, поэтому статья может содержать неточности, однако весь мой опыт изложенный ниже был неоднократно подтверждён на практике.

Итак, поехали!


## Установка

Для работы конфига необходимы следующие библиотеки:

```bash
npm install -g webpack
npm install --save-dev webpack
```

Сам **webpack**. Устанавливать его следует глобально — в систему и локально — в проект. Глобальная установка даст возможность использовать команду ``webpack``, а локальная — использовать его как библиотеку.

```bash
npm install --save-dev babel-core babel-loader babel-preset-es2015 babel-preset-react babel-preset-stage-0 babel-preset-stage-1
```

Прежде всего, **babel** с набором плагинов, объединённых в *пресеты*, внедряющих поддержку стандарта [ES2015](http://www.ecma-international.org/publications/standards/Ecma-262.htm), react−а с его [JSX](https://facebook.github.io/react/docs/jsx-in-depth.html) и разных фич ES6/7.

```bash
npm install --save-dev css-loader style-loader sass-loader resolve-url-loader extract-text-webpack-plugin
```

Загрузчики, реализующие поддержку файлов со стилями и плагин для сохранения извлечённых стилей в отдельный файл.

```bash
npm install --save-dev react react-dom bootstrap-sass
```

И оставшиеся react и scss-версия bootstrap.


## Структура проекта

Привожу структуру проекта, в данном случае — для простого одностраничного приложения. Структура вашего проекта может разительно отличаться, но для целей демонстрации она подходит очень хорошо.

```
├── index.html
├── package.json
├── webpack.config.js
└── static
    ├── build
    │   ├── bundle.js
    │   └── styles.css
    ├── app.js
    └── main.scss
```

## Настройка

Сначала конфиг — потом пояснения.

```javascript
webpack = require('webpack');
path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


webpackConfig = {
    context: __dirname,
    entry: {
        bundle: './static/app.js',
        styles: './static/main.scss'
    },
    output: {
        filename: '[name].js',
        path: './static/build',
        library: '[name]'
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    devtool: '#cheap-module-source-map',
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: [/node_modules/],
                loader: "babel-loader",
                query: {
                    presets: ['es2015', 'react', 'stage-0', 'stage-1']
                }
            },
            {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader!resolve-url!sass-loader?sourceMap')
            },
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
            },
            {
                test: /\.woff2?$|\.ttf$|\.eot$|\.svg$|\.png|\.jpe?g|\.gif$/,
                loader: 'file-loader'
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('styles.css', {
            allChunks: true
        })
    ]
};
module.exports = webpackConfig;
```

Исходных файлов два — ``static/app.js`` и ``static/main.scss``. После запуска команды ``webpack`` произойдёт загрузка данных из них с помощью определённых в конфиге загрузчиков.

Файлы с расширениями *.js* и *.jsx* будут обработаны **babel**−ом:

- jsx-синтаксис react−а будет преобразован в обычный яваскрипт
- es6/7 синтаксис будет преобразован в es5

Для обработки *scss*−стилей используется набор лоадеров, в том числе **sass-loader**:

```javascript
{
    test: /\.scss$/,
    loader: ExtractTextPlugin.extract('style-loader', 'css-loader!resolve-url!sass-loader?sourceMap')
}
```

Здесь мы указываем, что все *.scss* файлы будут обработаны сначала **sass-loader**, который на выходе сгенерирует обычный css. Затем в дело вступает **resolve-url-loader**, задача которого найти относительные пути к файлам в css (например, в директиве ``url(../image.jpg)``) и преобразовать их в абсолютные (для этого обязательно нужно включить source-map в предыдущем загрузчике). Результат передаётся в **css-loader**, который непосредственно отвечает за поддержку css в webpack. В случае, если что-то пошло не так, использоваться будет **style-loader**.

Так, с загрузчиками понятно, а что такое ``ExtractTextPlugin``? Ответ — это плагин, который сохраняет полученный от загрузчиков текст (исходный код) в отдельные чанки.

А дальше можно сохранить текст из этих чанков в отдельный файл, в данном случае *styles.css*:

```javascript
new ExtractTextPlugin('styles.css', {
    allChunks: true
}),
```

Опция ``allChunks: true`` указывает, что нужно все чанки склеить и сохранить в один файл, иначе они будут сохранены в отдельные файлы.

После обработки, вебпак сгенерирует выходные файлы в директории ``./static/build/``:

```html
<link rel="stylesheet" href="/static/build/styles.css">
<script type="text/javascript" src="/static/build/bundle.js"></script>
```

В целом данная конфигурация подходит для разработки простых одностраничных приложений. На выходе получается несколько файлов со скриптами и стилями, которые можно подключить на страницу.

После загрузки бандла, его исходный код будет прочитан и исполнен интерпретатором javascript. Также, благодаря опции ``output.library`` **webpack** экспортирует загруженный модуль в переменную с названием секции в ``entry``, в данном случае — ``bundle``. Это очень удобно, так как ваш модуль подключается как библиотека и становится доступен в глобальной области видимости:

```html
<script>
// sayHello — функция, определённая в файле app.js
bundle.sayHello()
// или
window.bundle.sayHello();
</script>
```

Стоит учесть, что webpack может генерировать бандлы, которые при загрузке автоматически подключат нужные стили на страницу, это реализуется с помощью **style-loader** и особенно удобно при разработке приложений с большим числом страниц или react-компонентов.

На этом всё. Удачного кодинга!
