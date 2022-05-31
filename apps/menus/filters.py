import django_filters
from django.db.models import Q

from apps.menus.models import Dish


class DishFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_search', label="Search")

    def my_search(self, qs, name, value):
        return qs.filter(Q(name__icontains=value))

    class Meta:
        model = Dish
        fields = "__all__"
