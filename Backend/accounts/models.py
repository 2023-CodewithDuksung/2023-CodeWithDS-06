from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, user_id, password, nickname, email, department):
        if not user_id:
            raise ValueError('Users must have an id')
        user = self.model(
            user_id=user_id,
            nickname=nickname,
            email=email,
            department=department
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, **extra_fields):
        superuser = self.create_user(
            user_id=user_id,
            password=password,
            nickname=user_id,
            email=user_id+"@gmail.com",
            department="과학기술대학"
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=50, null=False, unique=True)
    nickname = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    department = models.CharField(max_length=50, null=False, blank=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return f"({self.id}) {self.nickname}"

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
