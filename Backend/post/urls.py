from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.single_post, name='detail'),
    path('create/', views.create_post, name='create'),
]