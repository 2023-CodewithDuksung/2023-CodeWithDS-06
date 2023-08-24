from django.urls import path
from . import views


urlpatterns = [
    # path('', AccountView.as_view(), name='account_management'),  # 로그인, 정보 수정, 회원 탈퇴
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('update_user/', views.update_user, name='update_user'),

]