from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentAuthorOrAdmin

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
        if slug:
            post = get_object_or_404(Post, slug=slug)
        else:
            post = None
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        serializer.save(author=self.request.user, post=post, parent=parent_comment)
