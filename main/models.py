# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    lname = models.CharField(max_length=30, blank=True, null=True)
    fname = models.CharField(max_length=30, blank=True, null=True)
    mname = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery'


class Flower(models.Model):
    flower_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to='images/', verbose_name='Фотография букета')
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flower'
        app_label = 'main'


class FlowerList(models.Model):
    flower_list_id = models.AutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    orders = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    flower = models.ForeignKey(Flower, models.DO_NOTHING, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'flower_list'


class OrderStatus(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_status'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    staff = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    order_status = models.ForeignKey(OrderStatus, models.DO_NOTHING, blank=True, null=True)
    delivery = models.ForeignKey(Delivery, models.DO_NOTHING, blank=True, null=True)
    payment_type = models.ForeignKey('PaymentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class PaymentType(models.Model):
    payment_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_type'


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    session = models.CharField(max_length=32, blank=True, null=True)
    lname = models.CharField(max_length=30, blank=True, null=True)
    fname = models.CharField(max_length=30, blank=True, null=True)
    mname = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    position = models.ForeignKey(Position, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'
