from django.shortcuts import render, redirect
from .utils import *
import hashlib


def index(request):
    if check_if_logged_in(request):
        return redirect('catalog')
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
        'is_admin': Staff.objects.get(login=request.COOKIES.get('login')).position.is_admin,
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
    if not check_if_logged_in(request):
        return redirect('index')
    return render(request, 'main/add_order.html', {
        'order_status': OrderStatus.objects.all(),
        'payment_type': PaymentType.objects.all(),
        'category': Category.objects.all(),
        'flowers': Flower.objects.all(),
    })


def edit_order(request):
    if not check_if_logged_in(request):
        return redirect('index')
    return render(request, 'main/edit_order.html', {
        'order_id': request.GET.get('order_id'),
        'order_status': OrderStatus.objects.all(),
        'payment_type': PaymentType.objects.all(),
        'category': Category.objects.all(),
        'flowers': Flower.objects.raw('CALL get_order_flowers(%s)', [request.GET.get('order_id')]),
        'order_info': Orders.objects.raw('CALL get_order_info(%s)', [request.GET.get('order_id')])[0],
    })


def add_staff(request):
    if not check_if_logged_in(request):
        return redirect('index')
    if Staff.objects.get(login=request.COOKIES.get('login')).position.is_admin == 0:
        return redirect('staff')
    return render(request, 'main/add_staff.html', {
        'positions': Position.objects.all(),
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
    if not check_if_logged_in(request):
        return redirect('index')
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
        if request.POST['flower_cnt_' + str(el.flower_id)] != '0':
            price += float(el.price) * float(request.POST['flower_cnt_' + str(el.flower_id)])
            flower_list = FlowerList(
                count= request.POST['flower_cnt_' + str(el.flower_id)],
                orders_id=order.order_id,
                flower_id=el.flower_id,
            )
            flower_list.save()
    order.price = price
    order.save()
    return redirect('orders')


def action_edit_order(request):
    if not check_if_logged_in(request):
        return redirect('index')
    order = Orders.objects.get(order_id=request.GET.get('order_id'))
    order.order_status_id = request.POST['order_status']
    order.payment_type_id = request.POST['payment_type']
    client = Client.objects.get(client_id=order.client_id)
    client.lname = request.POST['lname']
    client.fname = request.POST['fname']
    client.mname = request.POST['mname']
    client.save()
    delivery = Delivery.objects.get(delivery_id=order.delivery_id)
    delivery.date = request.POST['delivery_date']
    delivery.address = request.POST['delivery_address']
    delivery.save()
    all_flowers = Flower.objects.all()
    price = .0
    for el in all_flowers:
        if request.POST['flower_cnt_' + str(el.flower_id)] != '0':
            price += float(el.price) * float(request.POST['flower_cnt_' + str(el.flower_id)])
            flower_list = FlowerList(
                count=request.POST['flower_cnt_' + str(el.flower_id)],
                orders_id=order.order_id,
                flower_id=el.flower_id,
            )
            flower_list.save()
    order.price = price
    order.save()
    return redirect('orders')


def action_delete_order(request):
    if not check_if_logged_in(request):
        return redirect('index')
    order = Orders.objects.get(order_id=request.GET.get('order_id'))
    order.delete()
    return redirect('orders')


def action_add_staff(request):
    if not check_if_logged_in(request):
        return redirect('index')
    if Staff.objects.get(login=request.COOKIES.get('login')).position.is_admin == 0:
        return redirect('staff')
    staff = Staff(
        login=request.POST['login'],
        password=str(hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()),
        lname=request.POST['lname'],
        fname=request.POST['fname'],
        mname=request.POST['mname'],
        phone=request.POST['phonenumber'],
        position_id=request.POST['position'],
    )
    staff.save()
    return redirect('staff')