from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipes,
                            Tag)
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class FavoriteSerializer(serializers.ModelSerializer):
    """Favorite recipe serializer."""

    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    recipe = SlugRelatedField(
        slug_field='recipe',
        queryset=Recipes.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('author', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['author', 'recipe']
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagsSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Ingredients serializer."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientWriteSerializer(serializers.ModelSerializer):
    """The ingredient recorder serializer."""

    id = IngredientsSerializer()
    name = serializers.CharField(required=False)
    measurement_unit = serializers.IntegerField(required=False)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')

    def to_representation(self, instance):
        data = IngredientsSerializer(instance.ingredient).data
        data['amount'] = instance.amount
        return data


class RecipesSerializer(serializers.ModelSerializer):
    """Recipes serializer."""

    author = UserSerializer(
        many=False,
        read_only=True
    )
    ingredients = IngredientWriteSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True
    )
    tags = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return (not user.is_anonymous
                and recipe.favorite.filter(author=user).exists())

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return (not user.is_anonymous
                and recipe.cart.filter(author=user).exists())

    class Meta:
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipes


class RecipeSmallSerializer(serializers.ModelSerializer):
    """Serializer to display a list of recipes in subscriptions."""

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipes


class RecipesSerializerCreate(serializers.ModelSerializer):
    """Recipe Creation serializer."""

    author = UserSerializer(
        many=False,
        read_only=True
    )
    ingredients = IngredientWriteSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'ingredients',
            'author',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipes

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError(
                'The name of the recipe cannot be less than 3 characters.'
            )
        name = name[0].upper() + name[1:]
        is_exist = Recipes.objects.filter(
            author=self.context['request'].user,
            name=name
        ).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'You have already saved a recipe with this name.')
        return name

    def validate_text(self, text):
        if len(text) < 10:
            raise serializers.ValidationError(
                'Recipe is less than 10 characters.'
            )
        return text[0].upper() + text[1:]

    def validate(self, data):
        ingredients_data = self.initial_data.get('ingredients')

        if not ingredients_data:
            raise serializers.ValidationError(
                'Add at least one ingredient.'
            )

        ingredients_list = []
        for ingredient in ingredients_data:
            ingredient_id = ingredient['id']
            try:
                int(ingredient['amount'])
            except ValueError:
                raise serializers.ValidationError(
                    'The amount of ingredient can only be specified by number.'
                )
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    'Specify the weight/quantity of ingredients.'
                )

            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    f'No ingredient found with id={ingredient_id}!'
                )
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'The ingredients should not be repeated.'
                )
            ingredients_list.append(ingredient_id)
        return data

    def create_ingridients(self, ingredients_data, recipe):
        for ingredient in ingredients_data:
            IngredientInRecipe(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient.get('amount')
            ).save()

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = self.initial_data.get('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipes.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

        self.create_ingridients(ingredients_data, recipe)

        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        recipe.ingredients.clear()
        recipe.tags.clear()
        ingredients_data = self.initial_data.get('ingredients')
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        IngredientInRecipe.objects.filter(recipe=recipe).all().delete()
        self.create_ingridients(ingredients_data, recipe)
        return super().update(recipe, validated_data)


class ActionsSerializer(serializers.ModelSerializer):
    """Serializer for recipe management."""

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipes
