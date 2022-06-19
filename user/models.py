from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:  # 이런거 궁금했는데 이거 없으면 username이
            raise ValueError('Users must have an username')
        user = self.model(username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=50, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일주소", max_length=100)
    fullname = models.CharField("실명", max_length=20)
    join_date = models.DateField("가입일", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    #

    REQUIRED_FIELDS: []
    # admin 유저 로그인할때 정하는 것

    objects = UserManager()

    def __str__(self):
        return f'{self.username}/{self.email}/{self.fullname}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Hobby(models.Model):
    name = models.CharField("취미 이름", max_length=20)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, verbose_name="유저", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개")
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField(Hobby, verbose_name="취미")
    #hobby = models.ForeignKey(Hobby, verbose_name="취미", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}님의 프로필입니다."
