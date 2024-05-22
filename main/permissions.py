from rest_framework import permissions


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            paper_id = request.data.get('paper')
            return request.user.reviews.filter(paper_id=paper_id).exists()
        return True
