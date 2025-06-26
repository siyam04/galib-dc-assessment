from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="AI-Powered Content Curation API",
        default_version='v1',
        description="API for content curation, summarization, and AI-powered analysis.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
