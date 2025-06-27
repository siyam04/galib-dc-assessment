from rest_framework import viewsets, filters
from content.models import Content
from content.permissions import IsOwnerOrReadOnly
from content.serializers.content_serializers import ContentSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'metadata', 'summary', 'sentiment', 'topics', 'recommendations']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
