import django_filters
from .models import Paper


class PaperFilter(django_filters.FilterSet):
    class Meta:
        model = Paper
        fields = {
            'title': ['icontains'],
            'keywords': ['exact'],
        }
