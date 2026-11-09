# Каталог компьютерной техники

Приложение для учета товаров компьютерной техники на складе
и оформления заказов на них. Консольная версия (ПР3) дополнена
веб-интерфейсом на Django (ПР5), страницы переведены на шаблоны Django (ПР6),
данные перенесены в SQLite (ПР7), слой доступа к данным переведён на Django ORM (ПР9),
настроена административная панель Django, оптимизированы запросы ORM, добавлены вычисляемые поля,
slug-маршрутизация и контекстный процессор (ПР10).

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
- `Product` — товар (`id`, `name`, `category`, `manufacturer`, `price`, `quantity`, `is_large`, `slug`);
- `Order` — заказ (`id`, `product`, `quantity`, `status`).

## Используемые технологии

- Python 3.12+;
- Django 6.1 — веб-фреймворк, шаблоны DTL, Django ORM, миграции и Django Admin;
- django-debug-toolbar — профилирование и инспекция SQL-запросов ORM;
- Unidecode — транслитерация кириллических названий для генерации slug;
- SQLite — реляционная СУБД (целевая база данных `db.sqlite3` под управлением ORM);
- HTML, собственный CSS и JavaScript (`homepage/static/homepage/`), без сторонних фреймворков;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Возможности

В веб-интерфейсе и административной панели (ПР5–ПР10):

- полнофункциональная административная панель Django (`/admin/`) с тонкой настройкой всех моделей;
- просмотр списка товаров, фильтрация по категории, производителю и признаку крупного остатка;
- сортировка товаров, пагинация, редактирование остатка прямо в таблице админки (`list_editable`);
- просмотр карточки товара по уникальному англоязычному slug (`get_absolute_url()`);
- просмотр связанных заказов прямо в карточке товара через встроенную форму `OrderInline` (`TabularInline`);
- список заказов с фильтрацией по статусу (`active`, `cancelled`, `completed`), сортировкой и пагинацией;
- массовые действия в панели управления (`cancel_orders`, `restore_orders`);
- вычисляемое на уровне БД поле `is_large` (`GeneratedField`);
- глобальный контекстный процессор (`catalog_context`), передающий название и число товаров во все шаблоны;
- панель Django Debug Toolbar для контроля N+1 и оптимизации запросов (`select_related`, `annotate`, `F`);
- статистика склада и заказов через ORM-агрегации.

## Модели Django ORM (ПР10)

| Модель | Приложение | Поля | Связи и ограничения | Методы / свойства |
| :--- | :--- | :--- | :--- | :--- |
| `Category` | `products` | `id` (Auto PK), `name` (CharField, unique) | `ordering = ("name",)` | `__str__` |
| `Manufacturer` | `products` | `id` (Auto PK), `name` (CharField), `country` (CharField) | `ordering = ("name",)` | `__str__` |
| `Product` | `products` | `id` (Auto PK), `name` (CharField), `category` (FK), `manufacturer` (FK), `price` (DecimalField, help_text), `quantity` (PositiveIntegerField, help_text), `is_large` (GeneratedField), `slug` (SlugField, unique) | `category` → `Category` (`PROTECT`), `manufacturer` → `Manufacturer` (`PROTECT`) | `get_absolute_url()`, `save()`, `is_in_stock(min_q)`, `reduce_quantity(q)`, `increase_quantity(q)`, `in_stock`, `__str__` |
| `Order` | `orders` | `id` (Auto PK), `product` (FK), `quantity` (PositiveIntegerField, help_text), `status` (CharField, choices=Status.choices) | `product` → `Product` (`PROTECT`) | `OrderManager` (`active()`, `cancelled()`, `completed()`, `for_product()`), `cancel()`, `complete()`, `product_name`, `total`, `is_cancelled` (property), `__str__` |

Связи моделей:

```
Product ──(ForeignKey, PROTECT)──> Category
Product ──(ForeignKey, PROTECT)──> Manufacturer
Order   ──(ForeignKey, PROTECT)──> Product
```

## Настройки административной панели Django (ПР10)

- **`ProductAdmin`**:
  - `list_display`: `id`, `name`, `category`, `manufacturer`, `price`, `quantity`, `is_large`, `active_orders_count`, `site_link`;
  - `list_display_links`: `name`;
  - `list_editable`: `quantity`;
  - `search_fields`: `name`, `category__name`, `manufacturer__name`;
  - `list_filter`: `category`, `manufacturer`, `is_large`;
  - `ordering`: `name`;
  - `list_per_page`: 20;
  - `readonly_fields`: `id`, `slug`, `is_large`;
  - `inlines`: `OrderInline` (`TabularInline`, `extra=0`, `can_delete=False`);
  - `view_on_site`: `True` + метод `site_link` с `format_html`;
  - `list_select_related`: `category`, `manufacturer`;
  - `get_queryset`: аннотирование `active_orders_count` через `Count(orders, filter=Q(orders__status=ACTIVE))`.
- **`OrderAdmin`**:
  - `list_display`: `id`, `product`, `product_price`, `quantity`, `total_price`, `status`;
  - `list_display_links`: `id`;
  - `search_fields`: `product__name`, `product__category__name`, `product__manufacturer__name`;
  - `list_filter`: `status`, `product__category`;
  - `ordering`: `-id`;
  - `list_per_page`: 20;
  - `readonly_fields`: `id`, `total_price`;
  - `list_select_related`: `product`, `product__category`, `product__manufacturer`;
  - `autocomplete_fields`: `product`;
  - `actions`: `cancel_orders` (массовая отмена заказов), `restore_orders` (массовое восстановление заказов) с `message_user`.
- **`CategoryAdmin`** и **`ManufacturerAdmin`**:
  - вывод столбцов с подсчетом привязанных товаров (`products_count`) через `Count`, сортировка, поиск, постраничный вывод по 20 записей.

## Страницы веб-интерфейса

| URL                           | View-функция                    | Описание                                                                           |
| ----------------------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| `/`                           | `homepage.views.index`          | главная страница, навигация с глобальным счетчиком товаров                         |
| `/products/`                  | `products.views.product_list`   | список товаров с пагинацией; параметры `?category=<id>&sort=price\|name&page=<n>`   |
| `/products/<slug:slug>/`      | `products.views.product_detail` | карточка товара по уникальному slug (`get_object_or_404`), наличие на складе       |
| `/orders/`                    | `orders.views.order_list`       | список заказов со статусами и пагинацией; параметры `?status=...&sort=...&page=...` |
| `/orders/<int:order_id>/`     | `orders.views.order_detail`     | карточка заказа (`get_object_or_404`) с выгрузкой через `select_related`          |
| `/products/search/`           | `products.views.product_search` | поиск; параметры `?q=&min_price=&max_price=`                                       |
| `/products/statistics/`       | `products.views.statistics`     | сводка по складу и категориям через ORM `aggregate` и `annotate`                   |
| `/orders/statistics/`         | `orders.views.statistics`       | статистика заказов (всего, активных, отмененных, завершенных) через ORM            |
| `/admin/`                     | `admin.site.urls`               | встроенная административная панель Django                                          |
| `/__debug__/`                 | `debug_toolbar.urls`            | панель инструментов отладки Django Debug Toolbar (в режиме DEBUG)                 |

## База данных и миграции

Целевая база данных: `db.sqlite3`.
Схема управляется миграциями Django:
- `products`:
  - `0001_initial` — базовые модели `Category`, `Manufacturer`, `Product`;
  - `0002_product_is_large_product_slug_alter_product_price_and_more` — добавление `is_large` (`GeneratedField`), `slug`, `help_text`;
  - `0003_populate_product_slugs` — миграция данных (`RunPython`) для заполнения slug на основе Unidecode;
  - `0004_alter_product_slug` — установка ограничения уникальности `unique=True` на `slug`.
- `orders`:
  - `0001_initial` — базовая модель `Order`;
  - `0002_order_status` — добавление поля `status` со статусами `TextChoices`;
  - `0003_migrate_order_statuses` — миграция данных (`RunPython`) для переноса старых булевых значений `is_cancelled` в `status`;
  - `0004_remove_order_is_cancelled_alter_order_quantity` — удаление поля `is_cancelled`.

Импорт начальных данных: `python -m db.import_sqlite_to_orm`.

## Структура проекта

```
tech_catalog/
├── README.md
├── requirements.txt
├── setup.cfg
├── manage.py           — команды управления Django
├── main.py             — консольная версия (сохранена с ПР3)
├── storage.py          — загрузка и сохранение (JSON <-> объекты, консольная версия)
├── db/                 — слой SQLite и скрипты миграции: import_sqlite_to_orm.py
├── sql/                — schema.sql, queries.sql (ПР7)
├── utils.py            — вспомогательные функции ввода
├── catalog/            — пакет настроек Django-проекта
│   ├── settings.py     — настройки проекта (INSTALLED_APPS, MIDDLEWARE, TEMPLATES, INTERNAL_IPS)
│   ├── urls.py         — маршруты верхнего уровня (включая admin/ и __debug__/)
│   ├── asgi.py
│   └── wsgi.py
├── templates/          — общие шаблоны
│   ├── base.html
│   ├── 404.html
│   └── includes/navigation.html
├── homepage/           — главная страница
│   ├── templates/homepage/index.html
│   └── static/homepage/{css,js,img}/
├── products/           — каталог товаров
│   ├── admin.py        — настройки ProductAdmin, CategoryAdmin, ManufacturerAdmin, OrderInline
│   ├── apps.py         — ProductsConfig с verbose_name
│   ├── context_processors.py — catalog_context (site_name, products_count)
│   ├── models.py       — Category, Manufacturer, Product (GeneratedField, SlugField, get_absolute_url)
│   ├── tests.py        — Django TestCase для моделей и views products
│   ├── urls.py         — маршруты каталога (slug-маршрут detail)
│   ├── views.py        — product_list, product_detail, product_search, statistics
│   ├── templates/products/
│   └── migrations/
├── orders/             — заказы
│   ├── admin.py        — OrderAdmin (list_display, actions, filters, search, autocomplete)
│   ├── apps.py         — OrdersConfig с verbose_name
│   ├── models.py       — Order (Status TextChoices, OrderManager, OrderQuerySet)
│   ├── tests.py        — Django TestCase для заказов
│   ├── urls.py         — маршруты заказов
│   ├── views.py        — order_list, order_detail, statistics
│   ├── templates/orders/
│   └── migrations/
├── models/             — ООП-классы предметной области консольной версии (ПР3)
├── data/               — JSON-файлы и catalog.sqlite (ПР7)
└── tests/              — автоматизированные тесты pytest
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
- django-debug-toolbar;
- Unidecode;
- pytest;
- flake8.

Установка зависимостей (в виртуальном окружении):

```
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

Создание суперпользователя (для доступа к `/admin/`):

```
python manage.py createsuperuser
```

Веб-версия (Django):

```
python manage.py runserver
```

После запуска открыть в браузере:
- Основной сайт: <http://127.0.0.1:8000/>
- Административная панель: <http://127.0.0.1:8000/admin/>

## Запуск тестов и проверок

```
python manage.py check
python manage.py makemigrations --check
python manage.py test
pytest -v
flake8 .
```
