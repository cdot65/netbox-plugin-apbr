import django_filters
from django.db.models import Q
from extras.filters import TagFilter

from .models import Apbr


class ApbrFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    class Meta:
        model = Apbr
        fields = ['number', 'description', 'status', 'tenant', 'site']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(id__icontains=value)
                | Q(number__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
