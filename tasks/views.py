from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("This is My first Django APP!")

def contact(request):
    return HttpResponse("<h1 style='text-align: center; color:red';>Hello World!!</h1>")

def defaultHome(request):
    return HttpResponse("Default Home Page")

def show_task(request):
    return HttpResponse("This is Show task page!")