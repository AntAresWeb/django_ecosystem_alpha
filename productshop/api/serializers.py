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


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    ...


# class ContetnSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(source='ingredient.id')
#     name = serializers.CharField(source='ingredient.name', read_only=True)
#     measurement_unit = serializers.CharField(
#         source='ingredient.measurement_unit', read_only=True)
#     amount = serializers.IntegerField(
#         min_value=const.MIN_AMOUNT, max_value=const.MAX_AMOUNT)

#     class Meta:
#         model = Content
#         fields = ('id', 'name', 'measurement_unit', 'amount',)

#     def to_internal_value(self, data):
#         try:
#             id = int(data.get('id'))
#         except ValueError:
#             raise serializers.ValidationError(
#                 {'id': 'Должно быть числом.'}
#             )
#         if not id:
#             raise serializers.ValidationError(
#                 {'id': f'Это поле обязательно. Строка: {data}'}
#             )

#         try:
#             amount = int(data.get('amount'))
#         except ValueError:
#             raise serializers.ValidationError(
#                 {'amount': 'Количество должно быть числом.'}
#             )
#         if not amount:
#             raise serializers.ValidationError(
#                 {'amount': f'Это поле обязательно. Строка: {data}'}
#             )
#         if amount not in range(const.MIN_AMOUNT, const.MAX_AMOUNT + 1):
#             raise serializers.ValidationError(
#                 {'amount': (f'Количество должно быть в пределах от '
#                             f'{const.MIN_AMOUNT} до {const.MAX_AMOUNT}')}
#             )

#         return {
#             'id': id,
#             'amount': amount,
#         }


# class RecipeReadSerializer(serializers.ModelSerializer):
#     tags = TagSerialiser(many=True)
#     author = UserListSerializer(many=False)
#     ingredients = ContetnSerializer(many=True, source='contents')
#     is_favorited = serializers.SerializerMethodField(required=False)
#     is_in_shopping_cart = serializers.SerializerMethodField(required=False)

#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients',
#                   'is_favorited', 'is_in_shopping_cart', 'name',
#                   'image', 'text', 'cooking_time',)

#     def get_is_favorited(self, obj):
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             return False
#         return obj.favorites.filter(user=user).exists()

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             return False
#         return obj.shoppingcarts.filter(user=user).exists()


# class RecipeWriteSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для создания/изменения рецепта
#     cooking_time - валидация осуществляется на уровне модели
#     source='contents' используется для передачи кверисета recipe.contents,
#     содержащего Content-объекты, связанные с текущим объектом Recipe
#     """
#     ingredients = ContetnSerializer(
#         many=True,
#         source='contents'
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True
#     )
#     author = UserListSerializer(
#         many=False,
#         default=serializers.CurrentUserDefault()
#     )
#     image = Base64ImageField(required=False)
#     name = serializers.CharField()

#     class Meta:
#         model = Recipe
#         fields = ('name', 'id', 'tags', 'cooking_time',
#                   'text', 'ingredients', 'author', 'image')
#         validators = (
#             UniqueTogetherValidator(
#                 queryset=Ingredient.objects.all(),
#                 fields=('ingredients', )
#             ),
#         )

#     def to_representation(self, instance):
#         serializer = RecipeReadSerializer(
#             instance=instance,
#             context=self.context,
#             many=False
#         )
#         return serializer.data

#     def create(self, validated_data):
#         contents = validated_data.pop('contents')
#         tags = validated_data.pop('tags')
#         recipe = Recipe.objects.create(**validated_data)
#         recipe.author = self.context['request'].user
#         recipe.tags.add(*tags)

#         for content in contents:
#             recipe.ingredients.add(
#                 content.get('id'),
#                 through_defaults={'amount': content.get('amount')}
#             )
#         return recipe

#     def update(self, instance, validated_data):
#         instance.author = self.context['request'].user
#         contents = validated_data.pop('contents')

#         tags = validated_data.pop('tags')
#         instance.tags.clear()
#         instance.tags.add(*tags)

#         instance.ingredients.clear()
#         for content in contents:
#             instance.ingredients.add(
#                 content.get('id'),
#                 through_defaults={'amount': content.get('amount')}
#             )
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance

#     def validate_ingredients(self, value):
#         if len(value) < 1:
#             raise serializers.ValidationError(
#                 'Список ингредиентов пуст. В рецепте должны быть ингридиенты.'
#             )
#         ids = [content.get('id') for content in value]
#         dup_ids = [x for i, x in enumerate(ids) if i != ids.index(x)]
#         if len(dup_ids) > 0:
#             raise serializers.ValidationError(
#                 f'В списке ингредиентов есть дубликаты c id = {dup_ids}'
#             )
#         not_ids = list(set(ids) - set(
#             Ingredient.objects.all().values_list('id', flat=True))
#         )
#         if len(not_ids):
#             raise serializers.ValidationError(
#                 f'В базе нет ингредиентов с id = {not_ids}'
#             )
#         return value

#     def validate_tags(self, value):
#         if len(value) < 1:
#             raise serializers.ValidationError(
#                 'Список тэгов пуст. Нужно указать хотя бы один тэг.'
#             )
#         ids = [content.id for content in value]
#         dup_ids = [x for i, x in enumerate(ids) if i != ids.index(x)]
#         if len(dup_ids) > 0:
#             raise serializers.ValidationError(
#                 f'В списке тэгов присутствуют дубликаты c id = {dup_ids}'
#             )
#         return value

#     def validate_name(self, value):
#         mask = '[a-zA-Zа-яА-Я]'
#         if not bool(re.search(mask, value)):
#             raise serializers.ValidationError(
#                 'Наименование рецепта не содержит букв. Это неправильно!'
#             )
#         return value


# class RecipeShortSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time',)
#         read_only_fields = ('id', 'name', 'image', 'cooking_time',)


# class SubscribeSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='author.email')
#     id = serializers.IntegerField(source='author.id')
#     username = serializers.CharField(source='author.username')
#     first_name = serializers.CharField(source='author.first_name')
#     last_name = serializers.CharField(source='author.last_name')
#     is_subscribed = serializers.SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Subscribe
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed', 'recipes', 'recipes_count',)
#         read_only_fields = ('email', 'id', 'username', 'first_name',
#                             'last_name', 'is_subscribed', 'recipes',
#                             'recipes_count',)

#     def get_is_subscribed(self, obj):
#         return True

#     def get_recipes_count(self, obj):
#         count = obj.author.recipes.aggregate(Count('id'))
#         return count.get('id__count')

#     def get_recipes(self, obj):
#         recipes_limit = self.context['recipes_limit']
#         if recipes_limit > 0:
#             recipes = obj.author.recipes.all()[:recipes_limit]
#         else:
#             recipes = obj.author.recipes.all()
#         serializer = RecipeShortSerializer(instance=recipes, many=True)
#         return serializer.data


# class PasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(max_length=150)
#     current_password = serializers.CharField(max_length=150)

#     class Meta:
#         fields = ('new_password', 'current_password',)


# class LoginSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=150)
#     email = serializers.CharField(max_length=254)

#     class Meta:
#         fields = ('password', 'email',)