from django.contrib import admin

from .models import (Cart, Favourite, Follow, Ingredient, IngredientsInRecipe,
                     Recipe, Tag)


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


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientsInline]


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsInRecipe)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favourite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
