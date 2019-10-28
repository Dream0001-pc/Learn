#-*- coding=utf-8 -*-
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from models import *
from hashlib import sha1


#注册
def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)

def register_handle(request):
    #接收用户输入
    post = request.POST;
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    uallow = post.get('allow')
    if upwd != upwd2:
        return redirect('/user/register/')

    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录页面
    return render(request, 'df_user/login.html')

def register_exist(request):
    uname = request.GET.get('user_name')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


#登录
def login(request):
    uname = request.COOKIES.get('uname', '')
    if uname == '':
        checked = ''
    else:
        checked = 'checked'
    context = {
        'title': '用户登录',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
        'checked': checked}
    #print (type(str(reverse('login'))))
    #return render(request, reverse('login'), context)
    return render(request, 'df_user/login.html', context)

#处理登录请求
def login_handle(request):
    #接收请求信息
    post = request.GET
    username = post.get('user_name')
    pwd =post.get('pwd')
    jizhu = post.get('jizhu')
    if jizhu == None:
        jizhu = 0

    #根据用户名查询对象
    user = UserInfo.objects.filter(uname=username)
    # print ('查询用户名:%s数量:%d'%(username, len(user)))
    print (username)
    print (type(jizhu))
    if len(user) == 1:
        s1 = sha1()
        s1.update(pwd)
        upwd = s1.hexdigest()
        if upwd == user[0].upwd:
            context = {'url': '/user/info/'}
            red = JsonResponse(context)
            #记住用户名
            if int(jizhu) == 1:
                red.set_cookie('uname', username)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = username
            return red
        else:
            context = {
                'title': '用户登录',
                'error_name': 0,
                'error_pwd': 1,
                'uname': username,
                'upwd': pwd,
                'url': '/user/login/'}
            return JsonResponse(context)
    else:
        context = {
            'title': '用户登录',
            'error_name': 1,
            'error_pwd': 0,
            'uname': username,
            'upwd': pwd,
            'url': '/user/login/'}
        return JsonResponse(context)


#用户中心
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name']}
    return render(request, 'df_user/user_center_info.html', context)

def order(request):
    context = {'title': '用户中心'}
    return render(request, 'df_user/user_center_order.html', context)

def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.upostcode = post.get('upostcode')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心',
               'user': user}
    return render(request, 'df_user/user_center_site.html', context)












