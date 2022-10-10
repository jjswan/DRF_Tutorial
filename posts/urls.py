from django.urls import path 
from rest_framework import routers

from .views import CommentViewSet, PostViewSet, like_post #comment와 post는 viewset, like_post는 함수형 뷰임

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls + [
  path('like/<int:pk>/', like_post, name='like_post'),
]