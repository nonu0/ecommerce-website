from django.db import models
from django.contrib.auth.models  import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email = email,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
    user = models.EmailField(max_length=50,unique=True)
    username = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']