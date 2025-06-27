from django.urls import path
from rest_framework.routers import DefaultRouter
from content.views.ai_views import AIAnalysisView
from content.views.category_views import CategoryViewSet
from content.views.content_views import ContentViewSet
from content.views.user_views import (
    UserRegistrationView,
    UserListView,
    UserDetailView,
    AnalyticsView
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'content', ContentViewSet, basename='content')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),

    path('users/', UserListView.as_view(), name='user-list'),

    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),

    path('analytics/', AnalyticsView.as_view(), name='analytics'),

    path('ai/analyze/', AIAnalysisView.as_view(), name='ai-analyze'),
]

urlpatterns += router.urls
