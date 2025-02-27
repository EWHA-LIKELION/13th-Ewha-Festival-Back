from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정 및 삭제 가능
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 누구나 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        # 수정 및 삭제는 작성자만 가능
        return obj.author == request.user
