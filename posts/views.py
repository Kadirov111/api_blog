from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Tag, PostLike
from .serializers import PostSerializer, TagSerializer, PostLikeSerializer
from .permissions import IsPostAuthorOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        value = request.data.get('value')  # like/dislike
        like, created = PostLike.objects.update_or_create(
            post=post, user=request.user, defaults={'value': value})
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)