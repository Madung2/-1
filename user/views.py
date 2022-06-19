from django.shortcuts import render
from django.db import models
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate

# Create your views here.


class UserView(APIView):
    # 사용자 정보에 관한 클래스
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # 조회
        return Response({"message": "get method!!"})

    def post(self, request):
        # 생성
        return Response({"message": "post method!!"})

    def put(self, request):
        # 수정
        return Response({"message": "put method!!"})

    def delete(self, request):
        # 삭제
        return Response({"message": "delete method!!"})


class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다"})

        login(request, user)
        return Response({"message": "login success!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!"})
