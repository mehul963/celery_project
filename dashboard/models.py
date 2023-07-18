from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager,User
from django.db import models
from django.db.backends.signals import connection_created

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .tasks import assign_lead

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Address is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('password', make_password(password))
        user = self.model(email=email, **extra_fields)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, 
        **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Lead(models.Model):
    handlers=models.ManyToManyField(CustomUser)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=20)

@receiver(signal=post_save,sender=Lead)
def start_assign_lead(sender,instance,created,**kwargs):
    print(sender)
    if not created:
        return False
    print("LEAD ADDED")
    assign_lead.delay(instance.id)
    