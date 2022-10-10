from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Profile
from .models import Post, Comment
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  permission_classes = [CustomReadOnly]
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['author', 'likes']


  def get_serializer_class(self): #게시글을 단순히 보는 것인지, 작성하는 것인지 알아보기
    if self.action == 'List' or 'retrieve':
      return PostSerializer
    return PostCreateSerializer

  def perform_create(self, serializer):
    profile = Profile.objects.get(user=self.request.user) #게시글 작성을 요청한 유저가 로그인한 해당 유저인지 확인하기
    serializer.save(author=self.request.user, profile=profile)

@api_view(['GET'])
@permission_classes({IsAuthenticated})
def like_post(request, pk): #여기서의 pk는 게시글의 pk인 듯?
  post = get_object_or_404(Post, pk=pk) #해당 pk를 가진 게시글 객체 가져오기
  if request.user in post.likes.all(): #request를 보낸 유저가 post.likes에 들어온 유저이면, 즉 이미 좋아요를 누른 유저이면
    post.likes.remove(request.user)  #post.likes의 리스트에서 request 보낸 유저 객체 지우기. 즉 좋아요가 취소되는 것
  else:
    post.likes.add(request.user) #좋아요를 누르지 않은 유저이면 likes에 좋아요 포함
  
  return Response({'status':'ok'})


class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  permission_classes = [CustomReadOnly]

  def get_serializer_class(self): #코멘트를 단순히 보는 것인지, 작성하는 것인지 알아보기
    if self.action == 'list' or 'retrieve':
      return CommentSerializer

    return CommentCreateSerializer

  def perform_create(self, serializer): #댓글 작성을 요청한 유저가 로그인한 해당 유저인지 확인하기
    profile = Profile.objects.get(user=self.request.user)
    serializer.save(author=self.request.user, profile=profile)