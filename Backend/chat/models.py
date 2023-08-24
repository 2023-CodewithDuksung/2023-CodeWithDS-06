from django.db import models
from accounts.models import User
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatRoom(TimeStampedModel):
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='sender_user', related_name='sender_user')
    sender_unread_count = models.IntegerField("보낸 사람이 읽지 않은 개수")

    receiver_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='receiver_user', related_name='receiver_user')
    receiver_unread_count = models.IntegerField("받는 사람이 읽지 않은 개수")

    latest_text = models.CharField('마지막 메시지', max_length=1000)


class Message(TimeStampedModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_column='room', related_name='room_message')
    is_from_sender = models.BooleanField("보낸 사람이 메시지를 보냈는지 여부")
    text = models.CharField('메시지', max_length=1000)
    read = models.BooleanField('받는 사람이 읽음 여부')