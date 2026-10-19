# Каталог компьютерной техники

Приложение для учета товаров компьютерной техники на складе
и оформления заказов на них. Консольная версия (ПР3) дополнена
веб-интерфейсом на Django (ПР5), страницы переведены на шаблоны Django (ПР6), данные перенесены в SQLite (ПР7).

## Назначение

Приложение ведет каталог товаров (ноутбуки, мониторы, периферия
и т. д.), отслеживает остатки на складе и позволяет оформлять
и отменять заказы на товары с проверкой доступного количества.

## Целевая аудитория

Небольшой магазин или склад компьютерной техники, которому нужен
простой инструмент учета товаров и заказов.

## Предметная область

Учет товаров компьютерной техники: категории, производители, цены,
остатки на складе и заказы клиентов на эти товары.

## Основные сущности

- `Category` — категория (`id`, `name`);
- `Manufacturer` — производитель (`id`, `name`, `country`);
- `Product` — товар (`id`, `name`, `category`, `manufacturer`, `price`, `quantity`);
- `Order` — заказ (`id`, `product`, `quantity`, `is_cancelled`).

## Используемые технологии

- Python 3.12+;
- Django 6.1 — веб-фреймворк;
- Django Template Language — шаблоны страниц;
- HTML, собственный CSS и JavaScript (`homepage/static/homepage/`), без фреймворков;
- SQLite и стандартная библиотека `sqlite3` — хранение данных веб-версии;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Возможности

В веб-интерфейсе (ПР5–ПР7) доступно только чтение данных:

- просмотр списка товаров, фильтрация по категории и сортировка по цене или названию;
- просмотр карточки товара с признаком наличия на складе;
- просмотр списка заказов (фильтр по состоянию) и карточки заказа со статусом;
- поиск товаров по названию и диапазону цен;
- статистика склада и заказов.

В консольной версии (ПР3) реализовано:

- просмотр и поиск товаров по названию;
- фильтрация по категории и по диапазону цен;
- сортировка товаров по цене или названию;
- проверка наличия товара на складе;
- оформление и отмена заказов с проверкой доступности;
- статистика по каталогу (остатки, стоимость, средняя цена);
- добавление новых товаров в каталог.

## Классы

| Класс          | Атрибуты                                                      | Методы                                                                                                                 |
| -------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `Category`     | `id`, `name`                                                  | `__str__`, `from_data()`                                                                                               |
| `Manufacturer` | `id`, `name`, `country`                                       | `__str__`, `from_data()`                                                                                               |
| `Product`      | `id`, `name`, `category`, `manufacturer`, `price`, `quantity` | `is_in_stock(min_quantity)`, `reduce_quantity(q)`, `increase_quantity(q)`, `validate_price(price)` (static), `__str__` |
| `Order`        | `id`, `product`, `quantity`, `is_cancelled`                   | `cancel()` (возвращает товар на склад), `__str__`                                                                      |

Связи объектов:

```
Product ──> Category
Product ──> Manufacturer
Order   ──> Product
```

Заказ при создании списывает товар со склада, при отмене возвращает.
Отмененный заказ не удаляется, у него выставляется `is_cancelled`.

## Страницы веб-интерфейса

| URL                           | View-функция                    | Описание                                                    |
| ----------------------------- | ------------------------------- | ----------------------------------------------------------- |
| `/`                           | `homepage.views.index`          | главная страница, навигация                                 |
| `/products/`                  | `products.views.product_list`   | список товаров; параметры `?category=<id>&sort=price\|name` |
| `/products/<int:product_id>/` | `products.views.product_detail` | карточка товара, наличие на складе                          |
| `/orders/`                    | `orders.views.order_list`       | список заказов со статусами                                 |
| `/orders/<int:order_id>/`     | `orders.views.order_detail`     | карточка заказа                                             |
| `/products/search/`           | `products.views.product_search` | поиск; параметры `?q=&min_price=&max_price=`                |
| `/products/statistics/`       | `products.views.statistics`     | сводка по складу и категориям                               |
| `/orders/statistics/`         | `orders.views.statistics`       | заказано по товарам, популярные товары                      |

Если товар или заказ с указанным идентификатором не найден,
возвращается страница с кодом статуса 404.

Маршрутизация двухуровневая: `catalog/urls.py` подключает `urls.py`
приложений через `include()`. У приложений заданы пространства имён
(`app_name`), маршруты названы `list` и `detail`: `products:list`,
`products:detail`, `orders:list`, `orders:detail`, `homepage:index`.
Ссылки в шаблонах строятся через `{% url %}`.

## Шаблоны Django

View-функции готовят контекст и вызывают `render(request, шаблон, context)`,
HTML формируют шаблоны:

- `templates/base.html` — общий каркас с блоками `title` и `content`;
- `templates/includes/navigation.html` — навигация (`{% include %}`);
- `templates/404.html` — страница «не найдено» для `handler404`;
- `homepage/templates/homepage/index.html`;
- `products/templates/products/` — `product_list.html`, `product_detail.html`,
  `includes/product_card.html`;
- `orders/templates/orders/` — `order_list.html`, `order_detail.html`,
  `includes/order_status.html`.

Дочерние шаблоны наследуют `base.html` через `{% extends %}`. Используются
циклы `{% for %}…{% empty %}`, условия `{% if %}` (наличие товара, статус заказа)
и фильтры: `|length` («Всего товаров») и `|default`. Для несуществующего
товара или заказа шаблон показывает сообщение, а ответ имеет статус 404.

## Статические файлы

Находятся в `homepage/static/homepage/` и подключаются через `{% load static %}`
и `{% static %}`: `css/style.css`, `js/main.js` (текущий год в подвале),
`img/logo.svg` (логотип в навигации).

## База данных (ПР7)

Данные веб-версии хранятся в SQLite: `data/catalog.sqlite`. Схема создается
из `sql/schema.sql`, данные переносятся из JSON скриптом `db/import_json.py`
(`python -m db.import_json` пересоздает содержимое таблиц).

| Таблица         | Поля                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| `categories`    | `id` INTEGER PK, `name` TEXT                                                                           |
| `manufacturers` | `id` INTEGER PK, `name` TEXT, `country` TEXT                                                           |
| `products`      | `id` INTEGER PK, `name` TEXT, `category_id` FK, `manufacturer_id` FK, `price` REAL, `quantity` INTEGER |
| `orders`        | `id` INTEGER PK, `product_id` FK, `quantity` INTEGER, `is_cancelled` INTEGER (0 — активен, 1 — отменен) |

Внешние ключи: `products.category_id → categories.id`,
`products.manufacturer_id → manufacturers.id`, `orders.product_id → products.id`.

`db/database.py` создает соединение (`sqlite3.Row`, `PRAGMA foreign_keys = ON`),
`db/queries.py` загружает именованные запросы из `sql/queries.sql`
(`-- name: <имя>`). Значения передаются в запросы только параметрами `?`.

Запросы в `sql/queries.sql`:

| Запрос                 | Вид                         | Где используется              |
| ---------------------- | --------------------------- | ----------------------------- |
| `category_list`        | список                      | фильтр списка товаров         |
| `product_list`         | список, JOIN, WHERE         | `/products/`                  |
| `product_by_id`        | JOIN, WHERE                 | `/products/<id>/`             |
| `products_search`      | WHERE (несколько условий)   | `/products/search/`           |
| `order_list`           | список, JOIN, WHERE         | `/orders/`                    |
| `order_by_id`          | JOIN, WHERE                 | `/orders/<id>/`               |
| `active_orders_count`  | COUNT                       | `/orders/statistics/`         |
| `stock_summary`        | COUNT, SUM, AVG, MIN, MAX   | `/products/statistics/`       |
| `category_stats`       | LEFT JOIN, GROUP BY         | `/products/statistics/`       |
| `product_orders_stats` | LEFT JOIN, GROUP BY         | `/orders/statistics/`         |
| `popular_products`     | GROUP BY, HAVING            | `/orders/statistics/`         |

Консольная версия (ПР3) по-прежнему работает с JSON через `storage.py`.

## Структура проекта

```
tech_catalog/
├── README.md
├── requirements.txt
├── setup.cfg
├── manage.py           — команды управления Django
├── main.py             — консольная версия (сохранена с ПР3)
├── storage.py          — загрузка и сохранение (JSON <-> объекты, консольная версия)
├── db/                 — слой SQLite: database.py, queries.py, import_json.py
├── sql/                — schema.sql, queries.sql
├── utils.py            — вспомогательные функции ввода
├── catalog/            — пакет настроек Django-проекта
│   ├── settings.py
│   ├── urls.py         — маршруты верхнего уровня
│   ├── asgi.py
│   └── wsgi.py
├── templates/          — общие шаблоны
│   ├── base.html
│   ├── 404.html
│   └── includes/navigation.html
├── homepage/           — главная страница
│   ├── templates/homepage/index.html
│   └── static/homepage/{css,js,img}/
├── products/           — страницы товаров (templates/products/)
├── orders/             — страницы заказов (templates/orders/)
├── models/
│   ├── __init__.py
│   ├── category.py     — Category и функции над списком категорий
│   ├── manufacturer.py — Manufacturer и функции над списком производителей
│   ├── product.py      — Product и функции над списком товаров
│   └── order.py        — Order и функции над списком заказов
├── data/               — JSON-файлы (хранят id, а не вложенные объекты) и catalog.sqlite
└── tests/
    ├── test_products.py
    ├── test_categories.py
    ├── test_manufacturers.py
    ├── test_orders.py
    └── test_db.py
```

Приложения `homepage`, `products` и `orders` содержат `views.py` и `urls.py`;
их `models.py` пока пустые — Django-модели появятся при переходе на ORM.
Классы предметной области остаются в пакете `models/` (ПР3).

## Формат хранения данных

Исходные данные лежат в JSON-файлах каталога `data/`.
Консольная версия загружает их при запуске и сохраняет при выходе
(пункт меню «0. Выход»). Веб-версия читает данные из SQLite
(`data/catalog.sqlite`) и ничего не изменяет.

## Требования

- Python 3.12+ (требование Django 6.1);
- Django 6.1;
- pytest;
- flake8.

Установка зависимостей (в виртуальном окружении):

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск программы

Веб-версия (Django):

```
python manage.py runserver
```

После запуска открыть в браузере <http://127.0.0.1:8000/>

Консольная версия (сохранена):

```
python main.py
```

## Запуск тестов

```
pytest -v
```

## Проверка качества кода

```
flake8 .
```

## Текущее состояние и план развития

Реализовано (ПР5): Django-проект и три приложения, двухуровневая
маршрутизация, view-функции и страницы на данных ПР3, динамические
URL, обработка 404, навигация, собственный CSS.

Реализовано (ПР6): шаблоны Django (наследование, `include`, контекст,
циклы, условия, фильтры), именованные URL с пространствами имён,
статические CSS, JavaScript и изображение.

Реализовано (ПР7): база SQLite, схема и перенос данных из JSON, 11 SQL-запросов
(`sql/queries.sql`), страницы читают данные через `sqlite3`, поиск и статистика.
Django ORM пока не используется.

На следующих этапах планируется:

- перенос сущностей в Django ORM (модели и миграции);
- веб-формы: создание заказов, добавление товаров;
- реализация пользователей и ролей (менеджер склада, клиент);
- разработка REST API;
- контейнеризация приложения и настройка CI/CD.
