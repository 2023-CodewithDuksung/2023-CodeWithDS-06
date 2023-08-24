from django.urls import path
from . import views

urlpatterns = [
    # path('', AccountView.as_view(), name='account_management'),  # 로그인, 정보 수정, 회원 탈퇴
    path('', views.mypage, name='mypage'),

]