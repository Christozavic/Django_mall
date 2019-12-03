import os

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # User

# Create your views here.
from accounts.forms import UserLoginForm, UserRegisterForm, UserAddressForm
# from accounts.models import User
from accounts.models import UserAddress
from utils import constants
from utils.verify import VerifyCode


def user_login(request):
    """ 用户登录 """
    # 如果登陆是从其他页面跳转过来的，会带 next参数，如果有 next参数，登陆完成后，需要跳转到 next所对应的地址，否则跳转到首页上去
    next_url = request.GET.get('next', 'index')
    # 第一次访问 URL GET 展示表单，供用户输入
    # 第二次访问 URL，POST请求，对用户提交的数据进行操作
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        print(request.POST)
        client = VerifyCode(request)
        code = request.POST.get('vcode', None)
        result = client.validate_code(code)
        print('验证结果：', result)
        # 表单是否通过验证
        if form.is_valid():
            data = form.cleaned_data
            # user = User.objects.get(username=data['username'], password=data['password'])
            # request.session[constants.LOGIN_SESSION_ID] = user.id
            # return redirect('index')

            # 使用django-auth来实现登陆
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                # 登陆后的跳转
                return redirect(next_url)
        else:
            print(form.errors)
    # 第一次访问 URL，GRT请求，展示表单，供用户输入
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {
        'form': form,
        'next_url': next_url,
    })


def user_logout(request):
    """ 用户退出 """
    logout(request)
    return redirect('index')


def user_register(request):
    """ 用户注册 """
    if request.method == 'POST':
        form = UserRegisterForm(request=request, data=request.POST)
        if form.is_valid():
            # 调用注册方法
            form.register()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm(request)
    return render(request, 'register.html', {
        'form': form,
    })


@login_required
def address_list(request):
    """ 地址列表 """
    my_addr_list = UserAddress.objects.filter(user=request.user, is_valid=True)
    return render(request, 'address_list.html', {
        'my_addr_list': my_addr_list,
    })


@login_required
def address_edit(request, pk):
    """ 地址的新增和编辑 """
    user = request.user
    addr = None
    initial = {}
    # 如果pk是数字，则表示修改
    if pk.isdigit():
        addr = get_object_or_404(UserAddress, pk=pk, user=user, is_valid=True)
        initial['region'] = addr.get_region_format()
    if request.method == 'POST':
        form = UserAddressForm(request=request, data=request.POST, instance=addr, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        form = UserAddressForm(request=request, instance=addr, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


def address_delete(request, pk):
    """ 删除地址信息 """
    addr = get_object_or_404(UserAddress, pk=pk, is_valid=True, user=request.user)
    addr.is_valid = False
    addr.save()
    return HttpResponse('OK')
