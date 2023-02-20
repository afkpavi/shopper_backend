from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from uuid import uuid4

class AccountManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password, **kwargs):
        
        super_user_fields = ['is_superuser', 'is_staff', 'is_active']

        for field in super_user_fields:

            kwargs.setdefault(field, True)

            if kwargs.get(field) is not True:
                raise Exception(f'{field} must be True for super user')
            
        return self.create_user(email, password, **kwargs)
    

class Account(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(primary_key=True, null=False, default=uuid4)
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(null=False, max_length=15)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = AccountManager()

    def __str__(self) -> str:
        return self.name