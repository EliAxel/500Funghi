from django.contrib import admin
from django.urls import path, include, re_path
from .importa_dati import delete_db, init_db

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'|/', include('main.urls')),
]

#delete_db()
#init_db()