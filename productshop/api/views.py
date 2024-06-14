from api.routines import append_product, change_product, delete_product
from api.serializers import (CategoryListSerializer, ProductSerializer,
                             ProductSetShortSerializer,
                             ShoppingCartReadSerializer)
from django.shortcuts import get_object_or_404
from products.models import Category, Product, ProductSet, ShoppingCart
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CategoryResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategorySubcategoryListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = (AllowAny,)
    pagination_class = CategoryResultsSetPagination


class ProductResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = ProductResultsSetPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartReadSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        owner = self.request.user
        return ShoppingCart.objects.filter(owner=owner)

    @action(methods=['post'], detail=True)
    def clean(self, request, pk=None):
        shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
        ProductSet.objects.filter(shoppingcart=shoppingcart).delete()
        serialiser = ShoppingCartReadSerializer(
                    instance=shoppingcart, many=False)
        return Response(serialiser.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete', 'patch'], detail=True)
    def product(self, request, pk=None):
        shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
        context = {'method': request.method}
        serializer = ProductSetShortSerializer(
            data=request.data, context=context
        )
        if serializer.is_valid(raise_exception=True):
            match request.method:
                case 'POST':
                    append_product(shoppingcart, serializer.validated_data)
                case 'PATCH':
                    change_product(shoppingcart, serializer.validated_data)
                case 'DELETE':
                    delete_product(shoppingcart, serializer.validated_data)

        serialiser = ShoppingCartReadSerializer(
                    instance=shoppingcart, many=False)
        return Response(serialiser.data, status=status.HTTP_200_OK)
