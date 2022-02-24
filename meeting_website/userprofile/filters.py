from django.contrib.gis.db.models.functions import GeometryDistance
from django_filters.rest_framework import DjangoFilterBackend

from userprofile.models import CustomUser


class CustomFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('distance'):
            distance = request.query_params.get('distance')
            if request.user.location:
                queryset = CustomUser.objects.filter(location__dwithin=(request.user.location, distance)).annotate(
                    distance=GeometryDistance(request.user.location, 'location')).order_by('distance')
                return super().filter_queryset(request, queryset, view)
        else:
            return super().filter_queryset(request, queryset, view)
