from rest_framework import permissions

class createOrderPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == "POST":
                return True
        else:
            return False


class IsOwnerOrReadOnly_order(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.user.is_authenticated and request.method != "PUT":
            return True

        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return str(obj.profile) == str(request.user)

class IsOwnerOrReadOnly_profile(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.user.is_authenticated and request.method != "POST":
            return True

        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return str(obj.user) == str(request.user)

class IsOwnerOrReadOnly_user(permissions.BasePermission):
    def has_permission(self, request, view):

        return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        else:
            return False

class BalancePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
