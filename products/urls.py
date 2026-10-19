from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("search/", views.product_search, name="search"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:product_id>/", views.product_detail, name="detail"),
]
