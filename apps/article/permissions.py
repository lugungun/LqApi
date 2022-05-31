from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 所有用户权限
        if request.method in permissions.SAFE_METHODS:
            return True
        # 管理员
        return request.user.is_superuser
