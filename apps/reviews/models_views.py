from rest_framework import viewsets

from apps.shared.pagination import *
from apps.shared.permission import *
from apps.reviews.serializers import *


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrRead,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = MediumResultsSetPagination
    filter_fields = ('truck',)
