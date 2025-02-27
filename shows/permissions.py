from rest_framework.permissions import BasePermission
from .models import Show, OperatingHours

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Show):
            return request.user.show == obj
        
        elif isinstance(obj, OperatingHours):
            return request.user.show == obj.show