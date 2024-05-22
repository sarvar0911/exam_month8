from rest_framework import permissions


class IsReviewer(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow all users to view reviews
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_reviewer
