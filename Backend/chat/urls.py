from django.urls import path
from .views import *

urlpatterns = [
    path('', ChatRoomList.as_view(), name='chatroom_list'),
    path('<int:id>/', MessageList.as_view(), name='message_list'),
]