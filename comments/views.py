from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentAuthorOrPostAuthorOrAdminOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrPostAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)