from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect
import random
from .models import *


def redirect_with_get(url, query):
    base_url = reverse(url)
    query_string = urlencode(query)
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)


def create_session():
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = ''
    for i in range(32):
        s += random.choice(alphabet)
    return s


def check_if_logged_in(request):
    obj = Staff.objects.filter(login=request.COOKIES.get('login'))
    if obj.count() != 1 or obj[0].session != request.COOKIES.get('session'):
        return False
    return True