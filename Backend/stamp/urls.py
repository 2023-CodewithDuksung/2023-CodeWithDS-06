from django.urls import path
from . import views

app_name = 'stamp'

urlpatterns = [
    path('', views.index, name='index'),
]