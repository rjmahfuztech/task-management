from django.shortcuts import render
from django.http import HttpResponse

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
            'name': 'mahfuz',
            'age': 22,
            'address': 'rajshahi'
        }
    return render(request, "test.html",context)