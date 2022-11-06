from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from head.models import (
    Favorite,
    Ingredient,
    Recipe,
    Tag
)
from users.models import User
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
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
        methods=['post', 'delete'], detail=True,
        url_name='favorite',
    ) # permission_classes=(SelfEditUserOnlyPermission,)
    def favorite(self, request, pk):
        user = User.objects.get(id=1)    # user = User.objects.get(id=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            instance = user.favorites.get(recipe=recipe)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        favorite = Favorite.objects.create(
            recipe=recipe,
            user=user
        )
        favorite.save()
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
