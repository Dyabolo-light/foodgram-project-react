import webcolors

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Ingredient, Recipe, Tag


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название

    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


# class CatSerializer(serializers.ModelSerializer):
#    achievements = AchievementSerializer(many=True, required=False)
#    age = serializers.SerializerMethodField()
#    color = Hex2NameColor()

#    class Meta:
#        model = Cat
#        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'ach',
#                  'age')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeWriteSerializer(serializers.ModelSerializer):
    tag = SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        slug_field='slug'
    )
    ingredient = SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    ingredient = IngredientSerializer()
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe
        read_only_fields = ['__all__']
