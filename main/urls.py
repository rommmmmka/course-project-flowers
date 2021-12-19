from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('catalog', views.catalog, name="catalog"),
    path('staff', views.staff, name="staff"),
    path('orders', views.orders, name="orders"),
    path('add_order', views.add_order, name="add_order"),
    path('edit_order', views.edit_order, name="edit_order"),
    path('add_staff', views.add_staff, name="add_staff"),

    path('action_login', views.action_login, name="action_login"),
    path('action_logout', views.action_logout, name="action_logout"),
    path('action_add_order', views.action_add_order, name="action_add_order"),
    path('action_edit_order', views.action_edit_order, name="action_edit_order"),
    path('action_delete_order', views.action_delete_order, name="action_delete_order"),
    path('action_add_staff', views.action_add_staff, name="action_add_staff"),
]
