from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #primaty_key를 User의 pk로 설정하여 통합적으로 관리
  nickname = models.CharField(max_length=128)
  position = models.CharField(max_length=128)
  subjects = models.CharField(max_length=128)
  image = models.ImageField(upload_to='profile/', default='default.png')

@receiver(post_save, sender=User) #사용자의 프로필 객체를 하나 생성할 때마다 신호를 받아서 실행됨. 
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
