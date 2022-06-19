from rest_framework import serializers
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self, obj):#hobby모델에 대한 obj
        # print(obj)
        # user_list =[]
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.username)

        return [up.user.username for up in obj.userprofile_set.all()]

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True)  # MtoM이기 때문에 쿼리셋으로 들어감

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()  # 1to1이기 때문에 오브젝트로 들어감

    class Meta:
        model = UserModel
        # fields = "__all__"
        fields = ["username", "email", "fullname", "join_date", "userprofile"]
        # 유저프로필은 1:1이기 때문에 _set도 없이 그냥 불러와도 됨
        # 하지만 이번 경우에는 유저프로필시리어라이저를 불러올거임
