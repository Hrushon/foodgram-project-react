from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[MinValueValidator(settings.COEFF_ONE)]
    )

    class Meta:
        """
        Сортирует сообщения по id (сначала новые)
        и добавляет русские название в админке.
        """
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        """
        Добавляет русские название в админке.
        """
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        """
        Добавляет русские название в админке.
        """
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Промежуточная модель связи ингредиента и рецепта."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(settings.COEFF_ONE)]
    )

    class Meta:
        """
        Добавляет русские название в админке.
        """
        verbose_name = 'Ингредиент + рецепт'
        verbose_name_plural = 'Ингредиенты + рецепты'

    def __str__(self):
        return f'{self.ingredient} => {self.recipe}'


class TagRecipe(models.Model):
    """Промежуточная модель связи тега и рецепта."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        """
        Добавляет русские название в админке.
        """
        verbose_name = 'Тег + рецепт'
        verbose_name_plural = 'Теги + рецепты'

    def __str__(self):
        return f'{self.tag} => {self.recipe}'


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписываемый'
    )

    class Meta:
        """
        Добавляет русские названия в админке.
        """
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="prevent_self_subscription"
            )
        ]

    def __str__(self):
        return f'{self.user} => {self.author}'


class ShoppingCart(models.Model):
    """Модель cписка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buy',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='Рецепт'
    )

    class Meta:
        """
        Добавляет русские названия в админке.
        """
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} => {self.recipe}'


class Favorite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='lover',
        verbose_name='Рецепт'
    )

    class Meta:
        """
        Добавляет русские названия в админке.
        """
        verbose_name = 'Список избранных рецептов'
        verbose_name_plural = 'Списки избранных рецептов'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} => {self.recipe}'
