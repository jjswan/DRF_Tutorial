from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission): #프로필 관련한 permission. 해당 객체의 프로필 관련 permission. 프로필 조회는 누구나 가능, Put, Patch같이 프로필을 수정하는 것은 해당 유저만 
  def has_object_permission(self, request, view, obj): 
    if request.method in permissions.SAFE_METHODS: #SAFE_METHODS는 get, head, options
      return True
    return obj.user == request.user #SAFE_METHOD가 아닌 것은 객체의 유저와 요정으로 들어온 유저를 비교해서 같으면 통과시킴

