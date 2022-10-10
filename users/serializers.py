from dataclasses import field
from django.contrib.auth.models import User #Django의 기본 User 모델 호출
from django.contrib.auth.password_validation import validate_password #Django의 기본 패스워드 검증 도구 호출
from django.contrib.auth import authenticate #Django의 기본 authenticate함수로 아래에서 설정한 TokenAuth 방식으로 유저 인증
from rest_framework import serializers #시리얼라이저 호출
from rest_framework.authtoken.models import Token #settings.py에 등록했던 Token 모델 호출
from rest_framework.validators import UniqueValidator #이메일 중복 방지를 위한 검증 도구
from .models import Profile

#회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer): #회원가입 시리얼라이저. Django에서 정의하는 ModelSerializer을 상속
  email = serializers.EmailField(    #EmailField = 유효한 이메일 주소의 값을 확인하는 CharField
    required = True,  #회원가입 시 email은 반드시 넣게 할 것
    validators = [UniqueValidator(queryset=User.objects.all())], #유저 모델에서 데이터를 모두 불러와서 queryset에 넣고, 중복되는 이메일이 있는지 체크
  )
  password= serializers.CharField(
    write_only = True,
    required=True, 
    validators = [validate_password], #비밀번호 검증
  )

  password2 = serializers.CharField(write_only=True, required=True) #비밀번호 재확인


  class Meta:
    model = User #모델은 django의 기본 User 모델
    fields = ('username', 'password', 'password2', 'email') #모델에서 받아올 필드만 선언


  def validate(self, data):
    if data['password'] != data['password2'] :   #첫 번째로 등록한 pw와 확인차 등록한 pw의 일치 여부 확인
      raise serializers.ValidationError(  #일치하지 않으면 validationError 출동!
        {"password": "Password fields didn't match."})
    
    return data #pw가 일치할 때는 data를 return


  def create(self, validated_data): #유저를 생성하고 토큰을 생성
    user = User.objects.create_user(  #user모델 이용해서 user 객체 만들기
      username = validated_data['username'], #앞에서 선언한 fields들
      email = validated_data['email'],
    )

    user.set_password(validated_data['password']) #주어진 validated_data에서 pw 정보를 찾아서 password에 저장. 즉 사용자가 입력한 pw 정보를 password에 저장하는 것
    user.save()
    token = Token.objects.create(user=user) #토큰 생성
    return user


#로그인 시리얼라이저
class LoginSerializer(serializers.Serializer): #모델이 필요 없어서 그냥 직접 사용할 Field 지정
  username = serializers.CharField(required=True)
  password = serializers.CharField(required=True, write_only=True)  #write_only 옵션으로 클라이언트->서버 방향의 역직렬화 가능, 서버->클라이언트 방향의 직렬화는 불가능

  def validate(self, data): #검증하기
    user = authenticate(**data)
    if user:
      token = Token.objects.get(user=user) #유저에 해당하는 토큰 찾아서 생성하기
      return token
    raise serializers.ValidationError(
      {"error": "Unable to log in with provided credentials."}
    )


#profile 시리얼라이저(모델 확장)
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ("nickname", "position", "subjects", "image")
    



