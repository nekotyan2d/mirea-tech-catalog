-- Запросы TechCat. Формат: "-- name: <имя>" начинает запрос, который
-- загружается в Python через db.queries. Значения передаются параметрами ?.

-- name: category_list
-- Список категорий (выборка списка)
SELECT id, name
FROM categories
ORDER BY name;

-- name: product_list
-- Список товаров с категорией и производителем (JOIN).
-- Параметры: category_id (или NULL), category_id, sort ('name' или 'price')
SELECT
    products.id,
    products.name,
    products.price,
    categories.name AS category_name,
    manufacturers.name AS manufacturer_name
FROM products
JOIN categories ON products.category_id = categories.id
JOIN manufacturers ON products.manufacturer_id = manufacturers.id
WHERE (? IS NULL OR products.category_id = ?)
ORDER BY CASE WHEN ? = 'name' THEN products.name END, products.price;

-- name: product_by_id
-- Полная информация о товаре (JOIN + WHERE). Параметр: id товара
SELECT
    products.id,
    products.name,
    products.price,
    products.quantity,
    products.quantity > 0 AS in_stock,
    categories.name AS category_name,
    manufacturers.name AS manufacturer_name,
    manufacturers.country AS manufacturer_country
FROM products
JOIN categories ON products.category_id = categories.id
JOIN manufacturers ON products.manufacturer_id = manufacturers.id
WHERE products.id = ?;

-- name: products_search
-- Поиск товаров по названию и диапазону цен (WHERE с несколькими условиями).
-- Параметры: подстрока, min, min, max, max (min/max могут быть NULL)
SELECT id, name, price, quantity
FROM products
WHERE name LIKE '%' || ? || '%'
  AND (? IS NULL OR price >= ?)
  AND (? IS NULL OR price <= ?)
ORDER BY price;

-- name: order_list
-- Список заказов с товаром (JOIN), фильтр по состоянию (WHERE).
-- Параметры: is_cancelled (0, 1 или NULL для всех), is_cancelled
SELECT
    orders.id,
    orders.quantity,
    orders.is_cancelled,
    products.name AS product_name
FROM orders
JOIN products ON orders.product_id = products.id
WHERE (? IS NULL OR orders.is_cancelled = ?)
ORDER BY orders.id;

-- name: order_by_id
-- Информация о заказе (JOIN + WHERE). Параметр: id заказа
SELECT
    orders.id,
    orders.quantity,
    orders.is_cancelled,
    products.id AS product_id,
    products.name AS product_name,
    products.price * orders.quantity AS total
FROM orders
JOIN products ON orders.product_id = products.id
WHERE orders.id = ?;

-- name: active_orders_count
-- Количество активных заказов (агрегатная функция COUNT)
SELECT COUNT(*) AS orders_count
FROM orders
WHERE is_cancelled = 0;

-- name: stock_summary
-- Сводка по складу (COUNT, SUM, AVG, MIN, MAX)
SELECT
    COUNT(*) AS products_count,
    COALESCE(SUM(quantity), 0) AS total_quantity,
    COALESCE(SUM(price * quantity), 0) AS total_value,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products;

-- name: category_stats
-- Товары и остатки по категориям (LEFT JOIN + GROUP BY)
SELECT
    categories.name AS category_name,
    COUNT(products.id) AS products_count,
    COALESCE(SUM(products.quantity), 0) AS total_quantity
FROM categories
LEFT JOIN products ON products.category_id = categories.id
GROUP BY categories.id, categories.name
ORDER BY products_count DESC, categories.name;

-- name: product_orders_stats
-- Количество заказанных единиц по товарам, без отмененных (LEFT JOIN + GROUP BY)
SELECT
    products.name AS product_name,
    COUNT(orders.id) AS orders_count,
    COALESCE(SUM(orders.quantity), 0) AS ordered_quantity
FROM products
LEFT JOIN orders
    ON orders.product_id = products.id
    AND orders.is_cancelled = 0
GROUP BY products.id, products.name
ORDER BY ordered_quantity DESC, products.name;

-- name: popular_products
-- Товары, заказанных единиц которых не меньше заданного (GROUP BY + HAVING).
-- Параметр: минимальное количество
SELECT
    products.name AS product_name,
    SUM(orders.quantity) AS ordered_quantity
FROM products
JOIN orders ON orders.product_id = products.id
WHERE orders.is_cancelled = 0
GROUP BY products.id, products.name
HAVING SUM(orders.quantity) >= ?
ORDER BY ordered_quantity DESC;
