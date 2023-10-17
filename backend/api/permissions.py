from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    '''Доступ к изменению разрешен только автору и администратору.'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or (user.is_authenticated
                    and (obj.author == user or user.is_admin)))
