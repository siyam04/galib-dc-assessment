from rest_framework import viewsets, permissions, filters
from content.models import Category
from content.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Anyone can read, only logged-in users can create/update (DRF built-in).
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
