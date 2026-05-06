from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to read/edit it.
    Requires the model to have a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Allow only if the object's user matches the request's user
        return hasattr(obj, 'user') and obj.user == request.user
