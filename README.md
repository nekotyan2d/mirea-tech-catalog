# Каталог компьютерной техники

Приложение для учета товаров компьютерной техники на складе
и оформления заказов на них. Консольная версия (ПР3) дополнена
веб-интерфейсом на Django (ПР5), страницы переведены на шаблоны Django (ПР6),
данные перенесены в SQLite (ПР7), слой доступа к данным переведён на Django ORM (ПР9).

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
- Django 6.1 — веб-фреймворк, шаблоны DTL, Django ORM и миграции;
- SQLite — реляционная СУБД (целевая база данных `db.sqlite3` под управлением ORM);
- HTML, собственный CSS и JavaScript (`homepage/static/homepage/`), без сторонних фреймворков;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Возможности

В веб-интерфейсе (ПР5–ПР9):

- просмотр списка товаров, фильтрация по категории, сортировка по цене или названию и пагинация;
- просмотр карточки товара с признаком наличия на складе (404 при отсутствии);
- просмотр списка заказов (фильтр по состоянию), сортировка по номеру или товару и пагинация;
- просмотр карточки заказа со статусом и расчетной суммой (404 при отсутствии);
- поиск товаров по названию/производителю и диапазону цен;
- статистика склада и заказов через ORM-агрегации.

В консольной версии (ПР3) реализовано:

- просмотр и поиск товаров по названию;
- фильтрация по категории и по диапазону цен;
- сортировка товаров по цене или названию;
- проверка наличия товара на складе;
- оформление и отмена заказов с проверкой доступности;
- статистика по каталогу (остатки, стоимость, средняя цена);
- добавление новых товаров в каталог.

## Модели Django ORM (ПР9)

| Модель | Приложение | Поля | Связи и ограничения | Методы / свойства |
| :--- | :--- | :--- | :--- | :--- |
| `Category` | `products` | `id` (Auto PK), `name` (CharField, unique) | `ordering = ("name",)` | `__str__` |
| `Manufacturer` | `products` | `id` (Auto PK), `name` (CharField), `country` (CharField) | `ordering = ("name",)` | `__str__` |
| `Product` | `products` | `id` (Auto PK), `name` (CharField), `category` (FK), `manufacturer` (FK), `price` (DecimalField), `quantity` (PositiveIntegerField) | `category` → `Category` (`on_delete=PROTECT`, `related_name="products"`), `manufacturer` → `Manufacturer` (`on_delete=PROTECT`, `related_name="products"`) | `is_in_stock(min_q)`, `reduce_quantity(q)`, `increase_quantity(q)`, `in_stock`, `category_name`, `manufacturer_name`, `manufacturer_country`, `__str__` |
| `Order` | `orders` | `id` (Auto PK), `product` (FK), `quantity` (PositiveIntegerField), `is_cancelled` (BooleanField) | `product` → `Product` (`on_delete=PROTECT`, `related_name="orders"`) | `cancel()`, `product_name`, `total`, `__str__` |

Связи моделей:

```
Product ──(ForeignKey, PROTECT)──> Category
Product ──(ForeignKey, PROTECT)──> Manufacturer
Order   ──(ForeignKey, PROTECT)──> Product
```

## Страницы веб-интерфейса

| URL                           | View-функция                    | Описание                                                                           |
| ----------------------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| `/`                           | `homepage.views.index`          | главная страница, навигация                                                        |
| `/products/`                  | `products.views.product_list`   | список товаров с пагинацией; параметры `?category=<id>&sort=price\|name&page=<n>`   |
| `/products/<int:product_id>/` | `products.views.product_detail` | карточка товара, наличие на складе (`get_object_or_404`)                            |
| `/orders/`                    | `orders.views.order_list`       | список заказов со статусами и пагинацией; параметры `?status=...&sort=...&page=...` |
| `/orders/<int:order_id>/`     | `orders.views.order_detail`     | карточка заказа (`get_object_or_404`)                                              |
| `/products/search/`           | `products.views.product_search` | поиск; параметры `?q=&min_price=&max_price=`                                       |
| `/products/statistics/`       | `products.views.statistics`     | сводка по складу и категориям через ORM `aggregate` и `annotate`                   |
| `/orders/statistics/`         | `orders.views.statistics`       | статистика заказов и популярные товары через ORM                                   |

Если товар или заказ с указанным идентификатором не найден,
возвращается страница с кодом статуса 404 (`get_object_or_404`).

## База данных и миграции

Целевая база данных веб-версии: `db.sqlite3`.
Схема управляется миграциями Django (`products/migrations/`, `orders/migrations/`).
Исходная база данных SQLite сохранена в `data/catalog.sqlite`, а резервная копия — в `data/catalog_backup.sqlite`.
Перенос данных из `data/catalog.sqlite` в базу Django ORM выполняется скриптом `db/import_sqlite_to_orm.py` в рамках атомарной транзакции (`python -m db.import_sqlite_to_orm`).
Структуру таблиц исходной базы можно просмотреть с помощью `python -m db.inspect_source_db`.

## Структура проекта

```
tech_catalog/
├── README.md
├── requirements.txt
├── setup.cfg
├── manage.py           — команды управления Django
├── main.py             — консольная версия (сохранена с ПР3)
├── storage.py          — загрузка и сохранение (JSON <-> объекты, консольная версия)
├── db/                 — слой SQLite и скрипты миграции: database.py, queries.py, import_json.py, inspect_source_db.py, import_sqlite_to_orm.py
├── sql/                — schema.sql, queries.sql (ПР7)
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
├── products/           — каталог товаров (модели, views, urls, templates/products, migrations)
├── orders/             — заказы (модели, views, urls, templates/orders, migrations)
├── models/             — ООП-классы предметной области консольной версии (ПР3)
├── data/               — JSON-файлы и catalog.sqlite (ПР7)
└── tests/              — автоматизированные тесты pytest (32 теста)
    ├── test_products.py
    ├── test_categories.py
    ├── test_manufacturers.py
    ├── test_orders.py
    ├── test_db.py
    └── test_orm.py
```

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

Применение миграций:

```
python manage.py migrate
```

Импорт данных из SQLite в Django ORM:

```
python -m db.import_sqlite_to_orm
```

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

Реализовано (ПР9): модели Django ORM (`Category`, `Manufacturer`, `Product`, `Order`),
связи `ForeignKey` с `PROTECT`, миграции, перенос данных через `db.import_sqlite_to_orm`,
переход представлений на ORM (фильтрация, поиск, сортировка, агрегация, аннотирование,
постраничный вывод с сохранением GET-параметров через `{% querystring %}`), тесты в `tests/test_orm.py`.

На следующих этапах планируется:

- веб-формы: создание заказов, добавление товаров;
- реализация пользователей и ролей (менеджер склада, клиент);
- разработка REST API;
- контейнеризация приложения и настройка CI/CD.
