from django.db import models
from django.db.models.constraints import UniqueConstraint

from user.models import CustomUser


class Tag(models.Model):
    name = models.CharField(verbose_name='Тег', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', unique=True, max_length=50)
    color = models.CharField(verbose_name='Цвет', max_length=256)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=256)
    measurement_unit = models.CharField(verbose_name='Система измерения',
                                        max_length=10)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=256)
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    text = models.TextField()
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        related_name='recipes',
        verbose_name='Ингредиент',
        blank=False)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='media/', default='default.jpg')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Название рецепта')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='Ингредиент')
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favourite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Рецепт')

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_favourite')]


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'author'],
                                        name='user_author')]


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart')

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_cart')]
