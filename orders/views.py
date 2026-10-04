from django.utils.html import escape

from homepage.views import load_data, not_found, page
from models.order import find_order_by_id


def _status(order):
    if order.is_cancelled:
        return "отменен", "badge--muted"
    return "активен", "badge--ok"


def order_list(request):
    _, _, orders = load_data()
    items = ""
    for order in orders:
        status, badge = _status(order)
        items += f"""
        <li class="list__item">
            <a href="/orders/{order.id}/">Заказ №{order.id}: {escape(order.product.name)}</a>
            <span class="badge {badge}">{status}</span>
        </li>"""
    content = f'<h1>Заказы</h1><ul class="list">{items}</ul>'
    return page("Каталог – заказы", content)


def order_detail(request, order_id):
    _, _, orders = load_data()
    order = find_order_by_id(orders, order_id)
    if order is None:
        return not_found("Заказ", "/orders/", "к списку заказов")

    status, badge = _status(order)
    content = f"""
    <div class="card">
        <h2 class="card__title">Заказ №{order.id}</h2>
        <p>
            Товар:
            <a href="/products/{order.product.id}/">{escape(order.product.name)}</a>
        </p>
        <p>Количество: {order.quantity} шт.</p>
        <p>Статус: <span class="badge {badge}">{status}</span></p>
        <a href="/orders/" class="btn">к списку заказов</a>
    </div>
    """
    return page(f"Заказ №{order.id}", content)
