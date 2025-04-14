from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, PostLike, Tag, Category
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, TagSerializer, CategorySerializer
from .permissions import IsPostAuthorOrAdminOrReadOnly, IsLikeOwnerOrReadOnly, IsAdminOrReadOnly
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsPostAuthorOrAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [IsPostAuthorOrAdminOrReadOnly()]


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


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, IsLikeOwnerOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
