from django.contrib import admin

from .models import (Follow, Ingredient,  IngredientsInRecipe,
                     Recipe,  # ShoppingCart,
                     Tag,)


class IngredientsInline(admin.TabularInline):
   model = Recipe.ingredient.through
   extra = 0
   min_num = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
#    list_filter = ('author',)
#    search_fields = ('user',)


# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ('author', 'recipe')
#     list_filter = ('author',)
#     search_fields = ('author',)


# class ShoppingCartAdmin(admin.ModelAdmin):
#    list_display = ('author', 'recipe')
#    list_filter = ('author',)
#    search_fields = ('author',)


# class IngredientRecipeAdmin(admin.ModelAdmin):
#    list_display = ('id', 'recipe', 'ingredient', 'amount',)
#    list_filter = ('recipe', 'ingredient')
#    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
    # 'in_favorite',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
#    filter_horizontal = ('ingredients',)
    empty_value_display = '-пусто-'
    inlines = [IngredientsInline]

#    def in_favorite(self, obj):
#        return obj.favorite.all().count()

#    in_favorite.short_description = 'Добавленные рецепты в избранное'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsInRecipe)
admin.site.register(Follow, FollowAdmin)
# admin.site.register(Favourite, FavoriteAdmin)
# admin.site.register(ShoppingCart, ShoppingCartAdmin)
