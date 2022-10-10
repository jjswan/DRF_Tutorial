from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import Post, Comment

#댓글 가져오기 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(read_only=True) #아래 class Meta에 들어갈 profile 필드를 정의한 것. 이를 작성하지 않으면 profile 필드에 profile의 pk만 나타남. 
  #해당 댓글 작성자의 실제 프로필 정보를 전달해주기 위한 필드임. "nickname", "position", "subjects", "image"
  #댓글을 작성할 때 필수로 작성해야 하는 fields를 제외한 기본 정보 작성 시리얼라이저 

  class Meta:
    model = Comment
    fields = ('pk', 'profile', 'post', 'text') #pk는 해당 comment의 pk, profile은 댓글쓰는 유저의 profile

#댓글 쓰기 시리얼라이저
class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ('post', 'text') #post는 댓글을 다는 해당 게시글의 pk 임


class PostSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(read_only=True) #아래 class Meta에 들어갈 profile 필드를 정의한 것. 이를 작성하지 않으면 profile 필드에 profile의 pk만 나타남. 해당 글 작성자의 실제 
  #프로필 정보를 전달해주기 위한 필드임. "nickname", "position", "subjects", "image"
  #게시글을 작성할 때 필수로 작성해야 하는 fields를 제외한 기본 정보 작성 시리얼라이저
  comments = CommentSerializer(many=True, read_only=True) #위에서 정의한 댓글을 가져오는 것

  class Meta:
    model = Post
    fields = ('pk', 'profile', 'title', 'body', 'image','published_date', 'likes', 'comments') #pk는 해당 게시글의 pk

#게시글 작성 시리얼라이저
class PostCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('title', 'category', 'body', 'image')



