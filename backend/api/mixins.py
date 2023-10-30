from rest_framework import mixins, viewsets


class OnlyViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)