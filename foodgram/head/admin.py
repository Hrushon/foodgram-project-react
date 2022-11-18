from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Subscription, Tag, TagRecipe)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    readonly_fields = ('measurement_unit',)

    def measurement_unit(self, instance):
        return instance.ingredient.measurement_unit

    measurement_unit.short_description = ' Единица измерения'


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)
    inlines = (
        IngredientRecipeInline,
        TagRecipeInline
    )

    def favorite_count(self, instance):
        return instance.lover.count()

    favorite_count.short_description = 'Количество добавлений в избранное'


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Subscription)
admin.site.register(Tag)
admin.site.register(TagRecipe)
