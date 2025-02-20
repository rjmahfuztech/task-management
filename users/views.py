from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, ListView,CreateView,FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
User = get_user_model()

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


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/reset_password.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "A reset mail has been sent. Please check your E-mail.")
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/reset_password.html'
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, 'Your password reset Successful!')
        return super().form_valid(form)
    

def activate_user(request, user_id, token):
    user = User.objects.get(id=user_id)
    if default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('sign-in')


# Admin dashboard view
admin_dashboard_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(admin_dashboard_decorators, name="dispatch")
class AdminDashboardView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin/dashboard.html'

    def get_queryset(self):
        queryset = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')    
        ).all()
        for user in queryset:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No group assigned'
        return queryset


# Assign role view
assign_role_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(assign_role_decorators, name="dispatch")
class AssignRoleView(FormView):
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    success_url = reverse_lazy('admin-dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        if role:
            self.user.groups.clear()
            self.user.groups.add(role)
            messages.success(self.request, f"User '{self.user.username}' has been assign to the '{role.name}' role.")
        else:
            messages.error(self.request, "Invalid Role selected!")
        return redirect(self.success_url)


# Create group view
create_group_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(create_group_decorators, name="dispatch")
class CreateGroupView(CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    context_object_name = 'form'
    success_url = reverse_lazy('create-group')

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group '{group.name}' has been created successful!")
        return super().form_valid(form)


# Group list view
group_list_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(group_list_decorators, name="dispatch")
class GroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        queryset = Group.objects.prefetch_related('permissions').all()
        return queryset
    

    
# User Profile
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['name'] = user.get_full_name()
        context['username'] = user.username
        context['email'] = user.email
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['last_login'] = user.last_login
        context['member_since'] = user.date_joined

        return context
    
# Edit UserProfile Info
'''
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    context_object_name = 'form'
    template_name = 'accounts/update_profile.html'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['form'] = self.form_class(instance=self.object, userprofile=user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
'''

@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    context_object_name = 'form'
    template_name = 'accounts/update_profile.html'

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')