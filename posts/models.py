from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile
# Create your models here.

class Post(models.Model): #게시글 모델
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  profile = models.ForeignKey(Profile, on_delete = models.CASCADE, blank=True)
  title = models.CharField(max_length = 128)
  category = models.CharField(max_length=128)
  body = models.TextField()
  image = models.ImageField(upload_to='post/', default='default.png')
  likes = models.ManyToManyField(User, related_name = 'like_posts', blank=True)
  published_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model): #댓글 달기 모델
  author = models.ForeignKey(User, on_delete = models.CASCADE) #댓글을 쓴 유저
  profile = models.ForeignKey(Profile, on_delete = models.CASCADE) #댓글을 쓴 유저의 프로필
  post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) #해당 게시글의 pk
  text=models.TextField()
