from django.shortcuts import render, redirect
from .forms import *
from .utils import *
from datetime import datetime
import hashlib


def index(request):
    return render(request, 'main/index.html', {
        'error_login': request.GET.get('error_login'),
        'error_password': request.GET.get('error_password'),
    })


def catalog(request):
    if not check_if_logged_in(request):
        return redirect('index')
    category_id = request.GET.get('category')
    return render(request, 'main/catalog.html', {
        'flowers': Flower.objects.filter(category_id=category_id),
        'categories': Category.objects.all(),
    })


def staff(request):
    if not check_if_logged_in(request):
        return redirect('index')
    return render(request, 'main/staff.html', {
        'staff': Staff.objects.raw("CALL get_staff()"),
        'login': request.COOKIES.get('login'),
    })


def orders(request):
    if not check_if_logged_in(request):
        return redirect('index')
    orders = Orders.objects.raw('CALL get_all_orders()')
    staff_id = Staff.objects.get(login=request.COOKIES.get('login')).staff_id
    if request.GET.get('personal_orders') == 'True':
        orders = Orders.objects.raw('CALL get_orders(%s)', [staff_id])
    return render(request, 'main/orders.html', {
        'personal_orders': request.GET.get('personal_orders'),
        'orders': orders,
    })


def add_order(request):
    return render(request, 'main/add_order.html', {
        'order_status': OrderStatus.objects.all(),
        'payment_type': PaymentType.objects.all(),
        'category': Category.objects.all(),
        'flowers': Flower.objects.all(),
    })


def action_login(request):
    if Staff.objects.filter(login=request.POST['login']).count() != 1:
        return redirect_with_get('index', {'error_login': True})
    password = str(hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest())
    obj = Staff.objects.get(login=request.POST['login'])
    if obj.password != password:
        return redirect_with_get('index', {'error_password': True})
    response = redirect('catalog')
    session = create_session()
    response.set_cookie('login', request.POST['login'])
    response.set_cookie('session', session)
    obj.session = session
    obj.save()
    return response


def action_logout(request):
    response = redirect('index')
    response.delete_cookie('login')
    response.delete_cookie('session')
    return response


def action_add_order(request):
    client = Client(
        lname=request.POST['lname'],
        fname=request.POST['fname'],
        mname=request.POST['mname'],
        phone=request.POST['phonenumber'],
    )
    client.save()
    delivery = Delivery(
        date=request.POST['delivery_date'],
        address=request.POST['delivery_address'],
    )
    delivery.save()
    order = Orders(
        staff_id=Staff.objects.get(login=request.COOKIES.get('login')).staff_id,
        client_id=client.client_id,
        order_status_id=request.POST['order_status'],
        delivery_id=delivery.delivery_id,
        payment_type_id=request.POST['payment_type'],
    )
    order.save()
    all_flowers = Flower.objects.all()
    price = .0
    for el in all_flowers:
        if request.POST['flower_cnt_' + str(el.flower_id)] is not None:
            price += float(el.price) * float(request.POST['flower_cnt_' + str(el.flower_id)])
            flower_list = FlowerList(
                count= request.POST['flower_cnt_' + str(el.flower_id)],
                orders_id=order.order_id,
                flower_id=el.flower_id,
            )
    order.price = price
    order.save()

    return redirect('orders')