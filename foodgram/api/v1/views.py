from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from head.models import (
    Ingredient,
    Recipe,
    Tag
)

from .filters import RecipeFilter
from .html2pdf import html_to_pdf
from .paginators import CustomPagination
from .permissions import IsAuthorOnlyPermission
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
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        if self.action == 'favorite':
            return FavoriteCreateSerializer
        if self.action == 'shopping_cart':
            return ShoppingCreateSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        elif self.request.method in (
            'PATCH', 'DELETE'
        ):
            self.permission_classes = (IsAuthorOnlyPermission,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'], detail=False,
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        context = user.buy.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(total=Avg('recipe__ingredientrecipe__amount'))
        return html_to_pdf('carttopdf.html', {'context': context})

    @action(
        methods=['post', 'delete'], detail=True,
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'DELETE':
            instance = user.favorites.filter(recipe=recipe)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Этот рецепт в списке отсутствует.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'recipe': pk
        }
        favorite = self.get_serializer(data=data)
        favorite.is_valid(raise_exception=True)
        favorite.save()
        serializer = FavoriteShoppingSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['post', 'delete'], detail=True,
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'DELETE':
            instance = user.buy.filter(recipe=recipe)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Этот рецепт в списке отсутствует.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'recipe': pk
        }
        shop_cart = self.get_serializer(data=data)
        shop_cart.is_valid(raise_exception=True)
        shop_cart.save()
        serializer = FavoriteShoppingSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
