from django_filters.rest_framework import (CharFilter, FilterSet,
                                           NumberFilter)

from head.models import Recipe


class RecipeFilter(FilterSet):
    """Кастомный фильтр для представления рецептов."""

    is_favorited = NumberFilter(
        field_name='lover__user', method='filter_users_lists'
    )
    is_in_shopping_cart = NumberFilter(
        field_name='buyer__user', method='filter_users_lists'
    )
    tags = CharFilter(method='tags_filter')

    def filter_users_lists(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous or not int(value):
            return queryset
        return queryset.filter(**{name: user})

    def tags_filter(self, queryset, name, value):
        return queryset.filter(**{name: value,}).distinct()

    class Meta:
        model = Recipe
        fields = (
            'author',
        )
