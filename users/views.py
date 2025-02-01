from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


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

@login_required
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
    
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {"users": users})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove Previous Role
            user.groups.add(role)
            messages.success(request, f"User '{user.username}' has been assign to the '{role.name}' role.")
            return redirect('admin-dashboard')
    
    return render(request, "admin/assign_role.html", {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form =CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' has been created successful!")
            return redirect('create-group')
        
    return render(request, "admin/create_group.html", {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()
    return render(request, "admin/group_list.html", {"groups": groups})