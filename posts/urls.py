from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagViewSet, PostLikeViewSet

router = DefaultRouter()
router.register('', PostViewSet, basename='post')
router.register('tags', TagViewSet, basename='tag')
router.register('likes', PostLikeViewSet, basename='post-like')

urlpatterns = [
    path('', include(router.urls)),
]
