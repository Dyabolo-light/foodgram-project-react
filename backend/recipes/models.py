from django.db import models
from django.db.models.constraints import UniqueConstraint

from user.models import CustomUser
# from .validators import validate_score, validate_year


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
    description = models.TextField()
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Тег',
        blank=True, null=True)
    ingredient = models.ManyToManyField(
        Ingredient, related_name='recipes',
        verbose_name='Ингредиент',
        blank=False)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')

    def __str__(self):
        return self.name

#    class Meta:
#        verbose_name = 'Произведение'
#        verbose_name_plural = 'Произведения'
#        indexes = [models.Index(fields=['year']),
#                   models.Index(fields=['name'])]


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        # related_name='follower',
        # verbose_name='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        # related_name='following',
        # verbose_name='Автор'
    )

    class Meta:
        unique_together = ('user', 'recipe')


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
        UniqueConstraint(fields=['user', 'author'], name='unique_follower')


# class Review(models.Model):
#    text = models.TextField(verbose_name='Текст отзыва')
#    pub_date = models.DateTimeField(verbose_name='Дата публикации',
#                                    auto_now_add=True)
#    author = models.ForeignKey(CustomUser,
#                               on_delete=models.CASCADE,
#                               related_name='reviews',
#                               verbose_name='Автор')
#    title = models.ForeignKey(
#        Title, on_delete=models.CASCADE,
#        related_name='reviews',
#        verbose_name='Произведение',
#        null=True)
#    score = models.IntegerField(
#        verbose_name='Оценка',
#        validators=[validate_score])

#    class Meta:
#        constraints = [
#            models.UniqueConstraint(
#                fields=['author', 'title'],
#                name='title_author_review'
#            )
#        ]

#    def __str__(self):
#        return self.text


# class Comment(models.Model):
#    author = models.ForeignKey(
#        CustomUser, on_delete=models.CASCADE,
#        related_name='comments',
#        verbose_name='Автор')
#    review = models.ForeignKey(
#        Review, on_delete=models.CASCADE,
#        related_name='comments',
#        verbose_name='Отзыв')
#    text = models.TextField(verbose_name='Текст')
#    pub_date = models.DateTimeField(
#        verbose_name='Дата публикации',
#        auto_now_add=True)
