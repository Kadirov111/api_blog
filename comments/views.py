from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentAuthorOrAdmin

from posts.models import Post

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrAdmin]

    def get_queryset(self):
        queryset = Comment.objects.all()
        slug = self.request.query_params.get('post_slug')
        if slug:
            post = get_object_or_404(Post, slug=slug)
            queryset = queryset.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        slug = self.request.data.get('slug', None)
        parent_id = self.request.data.get('parent', None)
        post = get_object_or_404(Post, slug=slug) if slug else None
        parent_comment = get_object_or_404(Comment, id=parent_id) if parent_id else None
        serializer.save(author=self.request.user, post=post, parent=parent_comment)