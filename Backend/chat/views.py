from datetime import datetime
from django.db.models import Subquery, DateTimeField, Q
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils.timezone import now
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
            room_id=F('id'),
            user1=F('receiver_user'),
            user2=F('sender_user'),
            unread_count=F('sender_unread_count'),
        ).values('user1','user2', 'unread_count', 'latest_text', 'modified')

        q2 = ChatRoom.objects.filter(receiver_user=user).annotate(
            room_id=F('id'),
            user1=F('sender_user'),
            user2=F('receiver_user'),
            unread_count=F('receiver_unread_count'),
        ).values('user1', 'user2', 'unread_count', 'latest_text', 'modified')

        union_subquery = q1.union(q2, all=True)

        queryset = ChatRoom.objects.filter(
            id__in=Subquery(union_subquery.values('id'))
        ).annotate(
            unread_modified=F('modified')
        ).order_by('-unread_modified')

        return union_subquery


def send_message(sender: User, receiver: User, text: str):
    if sender == receiver:
        return

    # 1. 내가 보낸 사람으로 만든 채팅 방이 있는지 확인한다.
    try:
        room = ChatRoom.objects.get(sender_user=sender, receiver_user=receiver)
        is_sender = True

    except ChatRoom.DoesNotExist:
        # 2. 내가 받는 사람으로 만든 채팅 방이 있는지 확인한다.
        try:
            room = ChatRoom.objects.get(sender_user=receiver, receiver_user=sender)
            is_sender = False

        except ChatRoom.DoesNotExist:
            # 3. 내가 보낸 사람으로 채팅 방을 만든다.
            room = ChatRoom.objects.create(
                sender_user=sender,
                sender_unread_count=0,
                sender_is_deleted=False,
                receiver_user=receiver,
                receiver_unread_count=0,
                receiver_is_deleted=False,
            )
            is_sender = True

    if is_sender:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=False,
            read=False,
        ).update(read=True, modified=now())

        # 메시지 발신 처리
        message = Message.objects.create(
            room=room,
            is_from_sender=True,
            text=text,
            read=False,
        )

        # 채팅 방 업데이트 처리
        room.sender_unread_count = 0
        room.sender_is_deleted = False
        room.receiver_unread_count += 1
        room.receiver_is_deleted = False
        room.latest_text = text
        room.save()

    else:
        # 이전 메시지 읽음 처리
        Message.objects.filter(
            room=room,
            is_from_sender=True,
            read=False,
        ).update(read=True, modified=now())

        # 메시지 발신 처리
        message = Message.objects.create(
            room=room,
            is_from_sender=False,
            text=text,
            read=False,
        )

        # 채팅 방 업데이트 처리
        room.sender_unread_count += 1
        room.sender_is_deleted = False
        room.receiver_unread_count = 0
        room.receiver_is_deleted = False
        room.latest_text = text
        room.save()


def message(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        sender = request.user  # 로그인된 사용자를 발신자로 설정

        room = ChatRoom.objects.get(id=request.POST['id'])
        receiver_id = None
        if room is not None:
            if room.sender_user == sender.id:
                receiver_id = room.receiver_user
            elif room.receiver_user == sender.id:
                receiver_id = room.sender_user
            else:
                render(request, 'chat/chatting.html')
        # 받는 사람은 예시로 'receiver_user'를 통해 가져오도록 설정
        receiver = User.objects.get(id=receiver_id)

        # 메시지 전송
        send_message(sender, receiver, text)

        # 필요한 리다이렉션 또는 응답 처리

    return render(request, 'chat/chatting.html')


class MessageList(ListView):
    model = Message
    template_name = 'chat/chattingin.html'  # 사용하려는 템플릿 파일 경로
    context_object_name = 'message_list'  # 템플릿에서 사용할 변수 이름
    ordering = '-pk'  # 정렬 기준