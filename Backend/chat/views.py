from datetime import datetime
from django.db.models import Subquery
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class ChatRoomList(ListView):
    model = ChatRoom
    template_name = 'chat/chatting.html'  # 사용하려는 템플릿 파일 경로
    context_object_name = 'room_list'  # 템플릿에서 사용할 변수 이름
    ordering = '-modified'  # 정렬 기준

    def get_queryset(self):
        user = self.request.user

        q1 = ChatRoom.objects.filter(sender_user=user).annotate(
            user=F('receiver_user'),
            unread_count=F('sender_unread_count'),
        ).values('user', 'unread_count', 'latest_text', 'modified')

        q2 = ChatRoom.objects.filter(receiver_user=user).annotate(
            user=F('sender_user'),
            unread_count=F('receiver_unread_count'),
        ).values('user', 'unread_count', 'latest_text', 'modified')

        q1_subquery = q1.annotate(
            modified_with_unread=Coalesce('modified', Value(datetime.min))
        ).values('user', 'unread_count', 'latest_text', 'modified_with_unread')

        q2_subquery = q2.annotate(
            modified_with_unread=Coalesce('modified', Value(datetime.min))
        ).values('user', 'unread_count', 'latest_text', 'modified_with_unread')

        union_subquery = q1_subquery.union(q2_subquery, all=True)

        queryset = ChatRoom.objects.filter(
            id__in=Subquery(union_subquery.values('id'))
        ).annotate(
            modified_with_unread=F('modified_with_unread')
        ).order_by('-modified_with_unread')

        return queryset

