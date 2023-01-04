# DRF
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):

    message = "You don't have permission to see this profile information"

    def has_object_permission(self, request, view, obj):
        return obj == request.user