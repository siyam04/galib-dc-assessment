from rest_framework.routers import DefaultRouter

from .views.category_views import CategoryViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls
