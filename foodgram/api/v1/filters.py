from django_filters.rest_framework import (
    ModelMultipleChoiceFilter,
    FilterSet,
    NumberFilter
)

from head.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Кастомный фильтр для представления рецептов."""

    is_favorited = NumberFilter(
        field_name='lover__user', method='filter_users_lists'
    )
    is_in_shopping_cart = NumberFilter(
        field_name='buyer__user', method='filter_users_lists'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )

    def filter_users_lists(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous or not int(value):
            return queryset
        return queryset.filter(**{name: user})

    class Meta:
        model = Recipe
        fields = (
            'author',
        )
