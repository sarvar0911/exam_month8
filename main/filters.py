import django_filters
from .models import Paper


class PaperFilter(django_filters.FilterSet):
    class Meta:
        model = Paper
        fields = {
            'title_uz': ['icontains'],
            'title_en': ['icontains'],
            'keywords_uz': ['exact'],
            'keywords_en': ['exact']
        }
