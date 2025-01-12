from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls'))
]


# Ctrl + Shift + p
# then, python select interpreter
# then recommended environment