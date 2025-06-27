from rest_framework.routers import DefaultRouter
from content.views.category_views import CategoryViewSet
from content.views.content_views import ContentViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'content', ContentViewSet, basename='content')

urlpatterns = router.urls
