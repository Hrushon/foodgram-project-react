from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from head.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

from .filters import RecipeFilter
from .html2pdf import html_to_pdf
from .paginators import CustomPagination
from .permissions import IsAuthorOnlyPermission
from .serializers import (FavoriteCreateSerializer, FavoriteShoppingSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCreateSerializer,
                          TagSerializer)


def custom_post_delete(self, request, pk, func_model):
    """Функция-обработчик POST, DELETE запросов """
    user = self.request.user
    recipe = self.get_object()
    if request.method == 'DELETE':
        instance = func_model.objects.filter(recipe=recipe, user=user)
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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Представление для рецептов, обрабатывающее GET, POST,
    PATCH, DELETE - запросы. Кроме этого, запросы POST, DELETE для
    изменения 'списка покупок' и 'списка избранных рецептов' пользователя.
    Также обрабатывает GET-запрос на скачивание списка покупок в PDF-файле.
    Настроена пагинация, устанавливать количество рецептов на страницу
    можно по параметру 'limit' (по умолчанию - 10 рецетов на страницу).
    Имеется возможность фильтровать результаты поиска по нескольким критериям:
    по автору рецепта, по тегу (slug-поле), по наличию рецепта в 'списке
    покупок' или 'списке избранного' у текущего пользователя.
    """

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
        func_model = Favorite
        return custom_post_delete(self, request, pk, func_model)

    @action(
        methods=['post', 'delete'], detail=True,
    )
    def shopping_cart(self, request, pk):
        func_model = ShoppingCart
        return custom_post_delete(self, request, pk, func_model)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тегов, обрабатывающее только безопасные запросы."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для ингредиентов, обрабатывающее только безопасные запросы.
    Доступен поиск ингредиентов по названию.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name', 'name')
