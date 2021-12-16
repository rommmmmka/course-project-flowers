from django.shortcuts import render, redirect
from .forms import *
from .utils import *
from datetime import datetime
import hashlib


def index(request):
    return render(request, 'main/index.html')


def orders_list(request):
    if not check_if_logged_in(request):
        return redirect('index')
    return 0


def action_login(request):
    if Staff.objects.filter(login=request.POST['login']).count() != 1:
        return redirect_with_get('index', {'error_login': True})
    password = str(hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest())
    obj = Staff.objects.get(login=request.POST['login'])
    if obj.password != password:
        return redirect_with_get('index', {'error_password': True})
    response = redirect('orders_list')
    session = create_session()
    response.set_cookie('login', request.POST['login'])
    response.set_cookie('session', session)
    return redirect('orders_list')


def action_logout(request):
    response = redirect('index')
    response.delete_cookie('login')
    response.delete_cookie('session')
    return response