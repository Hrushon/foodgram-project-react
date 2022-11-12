from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import (
    UserCreateSerializer
)

from head.models import Recipe, Subscription
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
        return (
            user.is_authenticated and bool(obj.subscriber.filter(user=user))
        )


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


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get(
            'recipes_limit', settings.COUNT_RECIPES_DEFAULT
        )
        recipes = obj.recipes.all()[:int(limit)]
        return FavoriteShoppingSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return bool(obj.subscriber.filter(user=user))

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки на автора."""

    class Meta:
        model = Subscription
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя.'
            )
        ]
