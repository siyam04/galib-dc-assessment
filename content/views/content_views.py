from rest_framework import viewsets, filters
from content.models import Content
from content.serializers import ContentSerializer
from content.permissions import IsOwnerOrReadOnly


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'metadata']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
