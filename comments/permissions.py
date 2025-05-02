from rest_framework import permissions

class IsCommentAuthorOrPostAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.author or
                request.user == obj.post.author or
                request.user.is_staff)