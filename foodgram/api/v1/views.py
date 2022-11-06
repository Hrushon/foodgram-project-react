from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from head.models import (
    Ingredient,
    Recipe,
    Tag
)
from users.models import User
from .serializers import (
    FavoriteShoppingSerializer,
    FavoriteCreateSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    ShoppingCreateSerializer,
    TagSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=1)
        serializer.save(author=user) # self.request.user

    @action(
        methods=['get'], detail=False,
    ) # permission_classes=(SelfEditUserOnlyPermission,)
    def download_shopping_cart(self, request):
        user = User.objects.get(id=1)  # user = User.objects.get(id=request.user)
        cart = user.buy.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(total=Avg('recipe__ingredientrecipe__amount'))



    @action(
        methods=['post', 'delete'], detail=True,
    ) # permission_classes=(SelfEditUserOnlyPermission,)
    def favorite(self, request, pk):
        user = User.objects.get(id=1) # user = User.objects.get(id=request.user)
        recipe = self.get_object()
        if request.method == 'DELETE':
            instance = user.favorites.filter(recipe=recipe)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Этот рецепт в списке избранного отсутствует.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'recipe': pk
        }
        favorite = FavoriteCreateSerializer(data=data)
        favorite.is_valid(raise_exception=True)
        favorite.save()
        serializer = FavoriteShoppingSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['post', 'delete'], detail=True,
    ) # permission_classes=(SelfEditUserOnlyPermission,)
    def shopping_cart(self, request, pk):
        user = User.objects.get(id=1) # user = User.objects.get(id=request.user)
        recipe = self.get_object()
        if request.method == 'DELETE':
            instance = user.buy.filter(recipe=recipe)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Этот рецепт в списке покупок отсутствует.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'recipe': pk
        }
        shop_cart = ShoppingCreateSerializer(data=data)
        shop_cart.is_valid(raise_exception=True)
        shop_cart.save()
        serializer = FavoriteShoppingSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
