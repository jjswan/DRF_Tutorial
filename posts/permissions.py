# from rest_framework import permissions

# class CustomReadOnly(permissions.BasePermission):
#   #글 조회는 누구나 가능, 생성은 로그인한 유저만, 편집은 해당 글 작성자만 가능
#   def has_permission(self, request, view):
#     if request.method == 'GET':
#       return True
#     return request.user.is_authenticated #로그인했는지를 인증하는 코드

#   def has_object_permission(self, request, view, obj):
#     if request.method in permissions.SAFE_METHODS:
#       return True
#     return obj.author == request.user #SAFE_METHOD가 아닌 것은 객체의 유저와 요청으로 들어온 유저를 비교해서 같으면 통과시킴
 
from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    ## 글 조회: 누구나, 생성: 로그인한 유저, 편집: 글 작성자
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
