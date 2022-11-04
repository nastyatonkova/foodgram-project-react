from django.db import models

from users.models import User


class Ingredient(models.Model):

    """Model of ingredients for recipes."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        "Name of the ingredient",
        max_length=150,
    )
    measurement_unit = models.CharField(
        "Unit of measure",
        max_length=50,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):

    """Model of tags for recipes."""
    name = models.CharField(
        "Tag",
        max_length=150,
    )
    color = models.CharField(
        "Unit of measure",
        max_length=50,
    )
    slug = models.SlugField(
        "Slug",
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
        "Recipe name",
        max_length=200,
    )
    image = models.TextField(
        "Image",
        blank=True,
        null=True,
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name="Ingredients",
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Ingredients"
    )
    text = models.TextField(
        "Recipe description",
        blank=True,
        null=True,
    )
    cooking_time = models.IntegerField(
        "Cooking time (in minutes)",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        "Recipe publication date",
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def display_tag(self):
        return ', '.join(tags.name for tags in self.tags.all()[:3])

    display_tag.short_description = 'Tag'


class IngredientInRecipe(models.Model):

    """Model for the number of products needed."""
    recipe = models.ForeignKey(
        to=Recipes,
        verbose_name="Recipe",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        verbose_name="Ingredient",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        "Number of ingredients",
        default=1,
    )

    class Meta:
        ordering = ('ingredient',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


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
        verbose_name="Recipe",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author}: {self.recipe}"


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
        verbose_name="Recipe",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author}: {self.recipe}"
