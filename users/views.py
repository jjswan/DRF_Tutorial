from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, ProfileSerializer
from .models import Profile
from .permissions import CustomReadOnly

# Create your views here.
class RegisterView(generics.CreateAPIView): #회원 생성 기능만 구현
  queryset=User.objects.all() #user 모델의 데이터 모두 가져오기
  serializer_class=RegisterSerializer

class LoginView(generics.GenericAPIView): #로그인 기능 구현. 모델 필요 없음 
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data #시리얼라이저에서 구현했던 validate()의 return값인 Token 받아옴
    return Response({"token": token.key}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
  permission_classes = [CustomReadOnly]
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer