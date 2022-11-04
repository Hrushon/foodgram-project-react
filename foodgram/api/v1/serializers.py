from rest_framework import serializers

from head.models import (
    Ingredient, Recipe, Tag
)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = '__all__'


# class RecipeRetriveSerializer(serializers.ModelSerializer):
#     """Сериализатор для одного рецепта."""
#     tags = TagSerializer(many=True, read_only=True)
#     author = serializers.SlugRelatedField(
#         slug_field="username",
#         read_only=True
#     )
#     ingredients = IngredientSerializer(many=True, read_only=True)
# 
#     class Meta:
#         model = Recipe
#         fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
