from rest_framework import mixins, viewsets


class ViewOnlyViewSet(
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                  ):
    """Viewset to handle GET requests only."""
    pagination_class = None
