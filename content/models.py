from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.ForeignKey(Category, related_name='contents', on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(blank=True, null=True)  # Flexible JSON-serializable data: tags, AI analysis results, custom attributes, etc.
    owner = models.ForeignKey(get_user_model(), related_name='contents', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Analyze automatically by Ai
    summary = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=128, blank=True, null=True)
    topics = models.JSONField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
