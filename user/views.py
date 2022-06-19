from django.shortcuts import render
from django.db import models
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.db.models import F
from user.models import UserProfile
from user.serializers import UserSerializer
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
# Create your views here.


class UserView(APIView):
    # 사용자 정보에 관한 클래스
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # 사용자 정보 조회
        user = request.user
        # 1. 역참조 사용하지 않았을때
        # user_profile = UserProfile.objects.get(user=user)
        # hobbys = user_profile.hobby.all()

        # 2. 역참조 사용했을 때
        # one -to-one field는 기본적으로 _set이 붙지 않아서 이런 형태가 된다
        # hobbys = user.userprofile.hobby.all()  # 오브젝트랑 쿼리셋을 str으로 바꿔서 보내는건 별로 바람직하지 않다
        # for hobby in hobbys:
        #     hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username= F('user__username')).values_list('username', flat=True)
        #     hobby_members = list(hobby_members)
        #     print(hobby.name, hobby_members)
        # hobbys = str(hobbys)
        all_users = UserModel.objects.all()
        return Response(UserSerializer(all_users, many=True).data)

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
