from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib.auth import authenticate, login, logout


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('Not valid both password!!!')
    return render(request, "registration/register.html", {'form':form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, "registration/login.html")

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')