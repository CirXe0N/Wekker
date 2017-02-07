from rest_framework import permissions


class UserCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT':
            return request.user.is_authenticated()
        if request.method == 'POST':
            return True
