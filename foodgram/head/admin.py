from django.contrib import admin

from .models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientRecipeInline,
        TagRecipeInline
    )


admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(TagRecipe)
