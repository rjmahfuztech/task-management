from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.set_password(form.cleaned_data.get('password'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail has been sent. Please check your E-mail.")
            return redirect('sign-in')
        else:
            print('Not valid both password!!!')
    return render(request, "registration/register.html", {'form':form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, "registration/login.html", {"form": form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, user_id, token):
    user = User.objects.get(id=user_id)
    if default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('sign-in')