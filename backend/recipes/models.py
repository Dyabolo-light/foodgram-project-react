from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
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
        max_length=200)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        blank=False)
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
        upload_to='media/', blank=False, null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def clean(self):
        if not self.cooking_time or self.cooking_time < 0:
            raise ValidationError('Нельзя приготовить блюдо мгновенно')


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
            name='recipe_ingredient')
        ]

    def clean(self):
        if not self.amount or self.amount < 0:
            raise ValidationError('Количество ингредиентов не может быть '
                                  'меньше 0')

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
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_user_author'),
            CheckConstraint(check=~models.Q(user=models.F('author')),
                            name='users_cannot_follow_themselves')
        ]


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart')

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_cart')]
