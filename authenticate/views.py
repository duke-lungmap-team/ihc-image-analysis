from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def login_view(request):
    if request.method == 'GET':
        if 'next' in request.GET:
            return render(
                request,
                'login.html',
                {'next': request.GET.get('next')}
            )
        else:
            return render(
                request,
                'login.html',
                {}
            )

    if request.method == 'POST' and request.POST.get('username') and request.POST.get('password'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if 'next' in request.POST:
                if request.POST['next'] == '':
                    return HttpResponseRedirect(reverse('home',))
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('home',))
        else:
            return HttpResponse('Login Failed', status=401)

    return render(
        request,
        'login.html',
        {}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def login_failed(request):
    return render(
        request,
        'login_failed.html',
        {}
    )
