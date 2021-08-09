from django_filters import rest_framework as filters
from .models import StarWarsFilesModel


class StarWarsFilesModelFilter(filters.FilterSet):

    character_name = filters.CharFilter()
    date_from = filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="date", lookup_expr="lt")

    class Meta:
        model = StarWarsFilesModel
        fields = ["character_name", "date_from", "date_to"]
