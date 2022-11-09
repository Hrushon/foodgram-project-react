import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from head.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagRecipe
)
from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return bool(obj.following.filter(user=user))


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSaveSerializer(serializers.Serializer):
    """Сериализатор для сохранения ингредиентов в рецепте."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для представления ингредиентов в рецепте."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    """Сериализатор декодирования картинки."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    author = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    ingredients = IngredientRecipeSaveSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author', 'ingredients',)

    def to_representation(self, value):
        return RecipeSerializer(value, context=self.context).data

    def create(self, validated_data):
        tags_list = validated_data.pop('tags')
        ingredient_list = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for item in ingredient_list:
            ingredient = get_object_or_404(Ingredient, id=item.get('id'))
            IngredientRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=item.get('amount')
            )
        for item in tags_list:
            TagRecipe.objects.create(
                tag=item,
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')

        tags_list = validated_data.pop('tags')
        instance.tags.set(tags_list)

        ingredient_list = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for item in ingredient_list:
            ingredient = get_object_or_404(Ingredient, id=item.get('id'))
            instance.ingredients.add(
                ingredient,
                through_defaults={'amount': item.get('amount')}
            )

        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""

    def __init__(self, *args, **kwargs):
        super(RecipeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.fields['author'].context['request'] = request

    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredientrecipe_set'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return bool(obj.lover.filter(user=user))

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return bool(obj.buyer.filter(user=user))


class FavoriteShoppingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сериализации рецептов, находящися в списке
    избранного и списке покупок.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'name',
            'image',
            'cooking_time'
        )


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в избранное."""

    class Meta:
        model = Favorite
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class ShoppingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в список покупок."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            )
        ]
