from rest_framework.permissions import BasePermission
from .models import Booth, OperatingHours

class IsManger(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Booth):
            return request.user.booth == obj
        
        elif isinstance(obj, OperatingHours):
            return request.user.booth == obj.booth