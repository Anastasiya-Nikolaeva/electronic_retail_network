from django_filters import rest_framework as filters

from .models import NetworkNode


class NetworkNodeFilter(filters.FilterSet):
    """
    Фильтр для узлов сети.

    Позволяет фильтровать узлы сети по стране и городу.
    """

    country = filters.CharFilter(field_name="country", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")

    class Meta:
        model = NetworkNode
        fields = ["country", "city"]
