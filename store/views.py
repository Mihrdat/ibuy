from django.db.models.aggregates import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)

from .serializers import (
    CollectionSerializer,
    ProductSerializer,
    CartSerializer,
)
from .models import (
    Collection,
    Product,
    Cart,
)
from .paginations import DefaultPagination


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'detail': 'Collection cannot be deleted, because it includes one or more products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
