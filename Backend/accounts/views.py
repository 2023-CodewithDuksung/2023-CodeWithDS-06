from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.forms import UserForm
from accounts.serializers import UserSerializer
from accounts.models import *


def signin(request):    # 로그인
    if request.method == "GET":
        return render(request, 'accounts/signin.html')

    elif request.method == "POST":
        user_id = request.POST['username']
        password = request.POST['password']
        # is_auto_login = request.POST['is_login']

        user = authenticate(user_id=user_id, password=password)
        if user is not None:
            login(request, user)

            # if is_auto_login:   # 자동 로그인 체크한 경우
            #     # 세션에 사용자 정보 저장
            #     request.session['user_id'] = user.user_id

            return redirect('mypage')
        else:
            return render(request, 'accounts/signin.html', {'error': 'ID or Password is not exists.'})
    else:
        return render(request, 'accounts/signin.html')


def signout(request):   # 로그아웃
    if request.method == "POST":
        logout(request)
    return redirect('home')


def signup(request):    # 회원가입
    print('signup 함수 실행!')
    if request.method == "GET":
        return render(request, 'accounts/signup.html')
    elif request.method == "POST":
        print('signup 함수 실행!')
        new_user = User.objects.create_user(
            user_id=request.POST['username'],
            password=request.POST['password'],
            nickname=request.POST['nickname'],
            email=request.POST['email'],
            department=request.POST['major']
        )
        new_user.save()

        return redirect('signin')
    else:
        return redirect('signup')


def delete_user(request):
    user = request.user
    user.delete()
    logout(request)  # 삭제 후 로그아웃

    return redirect('signin')  # 탈퇴 후 로그인 페이지로 리디렉션


def update_user(request):
    if request.method == "POST":
        input_user_id = request.POST['user_id']
        input_password = request.POST['password']

        user = request.user
        input_user = authenticate(user_id=input_user_id, password=input_password)




class AccountView(APIView):
    def post(self, request):    # 로그인
        user_id = request.data['user_id']
        password = request.data['password']
        is_auto_login = request.data['is_login']

        user = authenticate(user_id=user_id, password=password)
        if user is not None:
            login(request, user)  # 사용자 로그인

            if is_auto_login:   # 자동 로그인 체크한 경우
                # 세션에 사용자 정보 저장
                request.session['user_id'] = user.user_id

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User does not exists.'}, status=status.HTTP_204_NO_CONTENT)



