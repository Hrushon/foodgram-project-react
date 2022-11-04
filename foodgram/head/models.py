from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

COEFF_ONE = 1


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название"
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name="Картинка"
        )
    text = models.TextField(
        verbose_name="Описание"
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
        verbose_name="Тег"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин)",
        validators=[MinValueValidator(COEFF_ONE)]
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
        verbose_name="Название",
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения"
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
        verbose_name="Название",
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет",
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name="Слаг",
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
        verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(COEFF_ONE)]
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
        verbose_name="Тег"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт"        
    )

    class Meta:
        """
        Добавляет русские название в админке.
        """
        verbose_name = 'Тег + рецепт'
        verbose_name_plural = 'Теги + рецепты'

    def __str__(self):
        return f'{self.tag} => {self.recipe}'
