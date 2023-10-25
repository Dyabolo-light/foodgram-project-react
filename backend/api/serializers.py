from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favourite, Follow, Ingredient,
                            IngredientsInRecipe, Recipe, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['__all__']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__']


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipesByFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        model = CustomUser

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        serializer = RecipesByFollowingSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = AddIngredientSerializer(many=True,
                                          source='ingredients_in_recipe')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'ingredients',
                  'image', 'text', 'cooking_time')

    def add_tags_ingredients(self, ingredients, tags, model):
        for ingredient in ingredients:
            IngredientsInRecipe.objects.create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients_in_recipe')
        recipe = super().update(instance, validated_data)
        recipe.ingredients_in_recipe.all().delete()
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def validate(self, data):
        tags = data.get('tags')
        ingredients = data.get('ingredients_in_recipe')
        if not tags:
            raise ValidationError('Выберите тэги')

        if not ingredients:
            raise ValidationError('Добавьте ингредиенты')

        if len(tags) != len(set(tags)):
            raise ValidationError('Тэги должны быть уникальны')
        set_ingredients = set()
        for ingredient in ingredients:
            set_ingredients.add(ingredient.get('id'))
        if len(set_ingredients) != len(ingredients):
            raise ValidationError('Ингредиенты должны быть уникальны')

        return data


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        many=True,
        source='ingredients_in_recipe',
        read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favourite.objects.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Cart.objects.filter(recipe=obj).exists()
        return False


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        if Follow.objects.filter(
            author=data['author'], user=data['user']
        ).exists():
            raise ValidationError('Вы уже подписаны на этого автора')
        if data['author'] == data['user']:
            raise ValidationError('Нельзя подписаться на себя')
        return data

    def to_representation(self, instance):
        return FollowSerializer(instance.author, context=self.context).data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        if Cart.objects.filter(
            user=data['user'], recipe=data['recipe']
        ).exists():
            raise ValidationError('Ингредиенты уже в корзине')
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')
