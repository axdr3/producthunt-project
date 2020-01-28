from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def signup(request):

    if request.method == 'POST':
        #User has info and wants to create account
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.get(username=request.POST.get('username'))
                # return to signup page if username already exists, otherwise throw Exception
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST.get('username'), password=request.POST.get('password2') )
                auth.login(request, user)
                return redirect('home')
        else:
            user = User.objects.get(username=request.POST.get('username'))
            # return to signup page if username already exists, otherwise throw Exception
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})
    else:
        #User wants to enter info
        return render(request, 'accounts/signup.html')

def login(request):

    if request.method == 'POST':

        user = auth.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password1'))
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')



def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
