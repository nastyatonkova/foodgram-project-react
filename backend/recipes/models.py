from django.contrib.auth import get_user_model
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    """Model of ingredients for recipes."""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        'Name of the ingredient',
        max_length=150,
        unique=True,
    )
    measurement_unit = models.CharField(
        'Unit of measure',
        max_length=150,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Model of tags for recipes."""

    name = models.CharField(
        'Tag',
        max_length=150,
        db_index=True,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Color hex-code',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='The value entered is not a color in hex-format'
            ),
        ]
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Prescription list table model."""

    name = models.CharField(
        'Recipe name',
        max_length=200,
    )
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
        null=True,
        blank=True
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ingredients',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes',
    )
    text = models.TextField(
        'Recipe description',
        blank=True,
        null=True,
        validators=[
            MaxLengthValidator(9999, 'Maximum length of text')
        ],
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time (in minutes)',
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, 'Minimum cooking time'),
            MaxValueValidator(240, 'Maximum cooking time')
        ],
    )

    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        'Recipe publication date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_recipes',
            ),
        )

    def display_tag(self):
        return ', '.join(tags.name for tags in self.tags.all()[:3])

    display_tag.short_description = 'Tag'


class IngredientInRecipe(models.Model):
    """Model for the number of products needed."""

    recipe = models.ForeignKey(
        to=Recipes,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        'Number of ingredients',
        default=1,
        validators=[
            MinValueValidator(1, 'Minimum'),
        ]
    )

    class Meta:
        ordering = ('ingredient',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_on_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} {self.recipe.name}'


class Favorite(models.Model):
    """Favorite Recipe Model."""

    author = models.ForeignKey(
        User,
        verbose_name='Subscribed',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='favorite',
        verbose_name='Recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'recipe'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'{self.author.username}: {self.recipe.name}'


class Cart(models.Model):
    """Cart model."""

    author = models.ForeignKey(
        User,
        verbose_name='Subscribed',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='cart',
        verbose_name='Recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'recipe'),
                name='unique_cart',
            ),
        )

    def __str__(self):
        return f'{self.author.username}: {self.recipe.name}'
