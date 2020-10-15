from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,reverse
import requests
import json
import random
from .forms import LoginForm
from django.contrib.auth import logout,login,authenticate


def girl(request, page_num):
    res = requests.get('https://gank.io/api/v2/data/category/Girl/type/Girl/page/' + str(page_num) + '/count/10')
    text = json.loads(res.text)
    data = text['data']
    page_max = text['page_count']
    page_count = range(page_max)

    img_urls = []
    for girl in data:
        img_urls.append(girl['url'])
    random.shuffle(img_urls)
    context = {
        'img_urls': img_urls,
        'page_count': page_count,
        'page_num': page_num,
        'page_max': page_max
    }

    return render(request, 'meizi/meizi.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and user.is_active:
                login(request,user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('login'))
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


