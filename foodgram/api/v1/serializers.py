from rest_framework import serializers

from head.models import (
    Ingredient, Recipe, Tag
)

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'text',
            'cooking_time'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'measurement_unit'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = (
            'name',
            'color'
        )
