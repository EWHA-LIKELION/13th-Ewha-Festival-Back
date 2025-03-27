from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManagerOrReadOnly(BasePermission):
    """
    Notice 객체에 대한 수정/삭제 요청 시, 해당 Notice가 속한 부스를 담당하는
    사용자(로그인한 사용자의 booth와 Notice의 booth가 일치)를 허용합니다.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS 같은 안전한 메소드라면 모두 허용합니다.
        if request.method in SAFE_METHODS:
            return True
        
        # 요청한 사용자의 booth와 Notice의 booth가 동일한 경우에만 권한 허용
        return hasattr(request.user, 'booth') and obj.booth == request.user.booth
