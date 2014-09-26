[![Build Status](https://travis-ci.org/ITCase/django-unisender.svg?branch=master)](https://travis-ci.org/ITCase/django-unisender)
[![Coverage Status](https://coveralls.io/repos/ITCase/django-unisender/badge.png)](https://coveralls.io/r/ITCase/django-unisender)
[![Stories in progress](https://badge.waffle.io/itcase/django-unisender.png?label=in progress&title=In Progress)](https://waffle.io/itcase/django-unisender)
[![PyPI](http://img.shields.io/pypi/dm/django-unisender.svg)](https://pypi.python.org/pypi/django-unisender)

django-unisender
================

Интеграция django с сервисом рассылок [unisender](http://www.unisender.com)

## Возможности
* Работа с [API](http://www.unisender.com/ru/features/integration-api/) через интерфейс администратора
  * Создание и редактирование дополнительных полей сообщения
  * Создание и редактирование списков рассылки
  * Создание и редактирование подписчиков
  * Создание шаблонов писем
  * Создание рассылок
  * Просмотр статистики о рассылке


## [Документация](http://django-unisender.readthedocs.org/ru/latest/)

## Установка

```
pip install django-unisender
```

Добавить unisender в INSTALLED_APPS
```
INSTALLED_APPS = (
...
'unisender',
...
)
```

Добавить ключ для API unisender в settings.py. Ключ можно получить в личном кабинете unisender после регистрации.

```
UNISENDER_API_KEY = 'your_key'
```

Выполните:
```python manage.py syncdb```

либо если вы используете south
```python manage.py migrate unisender```

## Использование

### Настройки

* UNISENDER_API_KEY - ключ для работы с методами API
* UNISENDER_TEST_MODE - включает режим тестирования (в этом режиме запросы отправляются в unisender но ничего не записывается в их БД) по умолчанию False

### Cоздание рассылки

###### Для создания рассылки необходимо:
1. Создать список рассылки
2. Создать получателя (привязав его к списку рассылки)
3. Создать письмо
4. В личном кабинете на сайте unisender зарегистрировать email с которого будет происходить рассылка
5. Создать рассылку в качестве адреса отправителя необходимо указать email, который был зарегистрирован в пункте 4
6. Получить статус рассылки

## Планы на будущее
### Планируется реализовать
* Создание и отправка sms
* Отправка одиночного email сообщения без создания рассылки
* [Полный список issue](https://github.com/ITCase/django-unisender/issues?state=open)

### Невозможно реализовать в силу отсутствия методов API
* создание и редактирование тегов сообщений
* регистрация адреса электронной почты с которого производить рассылку

### Не планируется реализовывать в ближайшее время
* Раздел Методы для партнёрских сайтов

## Changelog
* 0.2.0 - В разработке;

* 0.1.7 - Поддержка django1.7;

* 0.1.6 - Исправление ошибок совместимости с django==1.5; рефакторинг; мелкие доработки;

* 0.1.5 - Добавлен helptext для списка контактов, начата работа над документацией исправление ошибок (26/07/2014);

* 0.1.4 - Добавлен tinymce4 в зависимости при установке приложения; добавлен вывод сообщения о том что включен тестовый режим; исправление ошибок (22/08/2014);

* 0.1.3 - Исправление ошибок (25/07/2014);

* 0.1.2 - Реализован метод API updateOptInEmail (25/07/2014);

* 0.1.1 - Исправлена ошибка с миграциями (24/07/2014);

* 0.1.0 - Добавлены кнопки перехода на страницы сайта unisender; добавлена статистика по переходу по ссылкам в письме (23/07/2014);

* 0.0.2 - Добавлены вложения к письмам исправление ошибок (22/07/2014);

* 0.0.1 - Начальная версия, базовый функционал;
