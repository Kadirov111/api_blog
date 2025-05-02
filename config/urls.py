from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('auth.urls')),
    path('api/categories/', include('category.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/users/', include('users.urls')),
]
