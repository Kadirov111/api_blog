from django.urls import path
from .views import UserProfileView, UserDetailView

urlpatterns = [
    path('me/', UserProfileView.as_view()),
    path('<str:username>/', UserDetailView.as_view()),
]