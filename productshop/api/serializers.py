import re

import core.constants as const
from django.db.models import Count, F, Sum
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from products.models import (
    Category, Image, Product, ProductSet, ShoppingCart, Subcategory
)


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug',)


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories',)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('file',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory.category')
    subcategory = serializers.CharField(source='subcategory.name')
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category',
                  'subcategory', 'price', 'images',)


class ProductSetSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')

    class Meta:
        model = ProductSet
        fields = ('product', 'product_name', 'product_price', 'quantity',)


class ShoppingCartReadSerializer(serializers.ModelSerializer):
    productset = ProductSetSerializer(source='productsets', many=True)
    total_products = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'owner', 'total_products', 'total_amount',
                  'total_quantity', 'productset',)

    def get_total_products(self, obj):
        return obj.productsets.count()

    def get_total_amount(self, obj):
        return obj.productsets.aggregate(
            total=Sum(F('product__price') * F('quantity')))['total']

    def get_total_quantity(self, obj):
        return obj.productsets.aggregate(
            total=Sum(F('quantity')))['total']


class ProductSetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSet
        fields = ('product', 'quantity',)

    def get_fields(self):
        fields = super().get_fields()
        if self.context['method'] == 'DELETE':
            fields.pop('quantity')
        return fields
