.. title: Установка postgresql в Ubuntu / Linux Mint
.. description: Как поставить postgres с поддержкой кодировки UTF-8
.. slug: ustanovka-postgresql-v-ubuntu-linut-mint
.. date: 2016-04-17 23:00:00 UTC+03:00


Во всех моих проектах используется **Postgresql** и каждый раз, когда необходимо её установить на чистую машину, приходится восстанавливать процесс установки.

Чтобы эту проблему решить, документирую процесс здесь.

## Установка

На данный момент я предпочитаю устанавливать самую свежую стабильную версию postgres из официального репозитория:

```bash
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
$ wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
```

Перед установкой я рекомендую выставить локаль ``ru_RU.UTF-8``.

```bash
export LC_ALL=ru_RU.UTF-8
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

## Пересоздание кластера

Для того, чтобы решить проблемы с упорядочиванием и фильтрацией кириллических строк, необходимо пересоздать кластер БД сразу после установки с корректными значениями локали и кодировки:


**ВНИМАНИЕ!** Приведённые ниже команды полностью удалят ваш текущий кластер со всеми данными:

```bash
pg_dropcluster 9.5 main --stop
pg_createcluster --locale=ru_RU.UTF-8 --encoding=UTF-8 --start 9.5 main
```

В данных командах версия **postgresql** — ``9.5``, название кластера — ``main``. Готово, можно работать.


## Альтернатива

В качестве альтернативы пересозданию кластера, можно вручную изменить кодировку шаблона ``template0``. Это будет работать только для новых баз данных.

```bash
# psql -U postgres

postgres=# update pg_database set datallowconn = TRUE where datname = 'template0';
UPDATE 1
postgres=# \c template0
You are now connected to database "template0".
template0=# update pg_database set datistemplate = FALSE where datname = 'template1';
UPDATE 1
template0=# drop database template1;
DROP DATABASE
template0=# create database template1 with template = template0 encoding = 'UTF8';
CREATE DATABASE
template0=# update pg_database set datistemplate = TRUE where datname = 'template1';
UPDATE 1
template0=# \c template1
You are now connected to database "template1".
template1=# update pg_database set datallowconn = FALSE where datname = 'template0';
UPDATE 1
```

Скрипт взят [отсюда](https://gist.github.com/ffmike/877447).
