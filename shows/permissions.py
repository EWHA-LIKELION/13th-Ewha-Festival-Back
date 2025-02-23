from rest_framework.permissions import BasePermission
from .models import Show, PerformanceSchedule

class IsManger(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Show):
            return request.user.show == obj
        
        elif isinstance(obj, PerformanceSchedule):
            return request.user.show == obj.show