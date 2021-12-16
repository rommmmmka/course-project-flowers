from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('orders_list', views.orders_list, name="orders_list"),

    path('action_login', views.action_login, name="action_login"),
]
