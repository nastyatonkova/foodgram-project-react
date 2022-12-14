from api.serializers import RecipeSmallSerializer
from rest_framework import serializers
from users.models import Subscription, User


class UserShowSerializer(serializers.ModelSerializer):
    """Serializer to output user/user list."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, username):
        user = self.context["request"].user
        return (not user.is_anonymous
                and Subscription.objects.filter(
                    user=user,
                    following=username
                ).exists())

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class UserSerializer(serializers.ModelSerializer):
    """Basic custom user serializer with additional fields."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'role'
        )

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "A user with this email is already registered."
            )

        return data

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "A user with this name already exists."
            )

        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class SignupSerializer(serializers.ModelSerializer):
    """Serializer registration."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    banned_names = ('me', 'admin', 'ADMIN', 'administrator', 'moderator')

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, data):
        if data in self.banned_names:
            raise serializers.ValidationError(
                "You can't use a name like that."
            )

        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "User already exists."
            )

        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "A user with this email is already registered."
            )

        return data


class TokenSerializer(serializers.Serializer):
    """TokenSerializer."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=24)


class SubShowSerializer(UserShowSerializer):
    """Serializer to output user/user list."""

    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        )

    def get_is_subscribed(self, username):
        """If we request this method, we are subscribed to user"""
        return True

    def get_recipes(self, data):
        """Getting user recipes."""
        limit = self.context.get('request').query_params.get('recipes_limit')
        if not limit:
            limit = 3
        recipes = data.following.recipes.all()[:int(limit)]
        return RecipeSmallSerializer(recipes, many=True).data
