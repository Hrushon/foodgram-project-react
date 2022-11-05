import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from head.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe
)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
#    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        #    'is_subscribed'
        )

    #def get_is_subscribed(self, obj):
    #    user = self.context.get('request').user
    #    return user in obj.following.all()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSaveSerializer(serializers.Serializer):
    """Сериализатор для сохранения ингредиентов в рецепте."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для представления ингредиентов в рецепте."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', required=False)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        required=False
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
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSaveSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author', 'ingredients',)

    def to_representation(self, value):
        return RecipeSerializer(value).data

    def create(self, validated_data):
        print(validated_data)
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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredientrecipe_set'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
