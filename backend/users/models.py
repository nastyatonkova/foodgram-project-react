from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    USER_ROLE = (
        (USER, 'User role'),
        (ADMIN, 'Administrator role'),
    )

    email = models.EmailField(
        'Email',
        unique=True,
        error_messages={
            'unique': ('This email is already registered'),
        }
    )

    first_name = models.TextField(
        'Name',
        max_length=150,
        blank=True,
    )

    last_name = models.TextField(
        'Last Name',
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        'Bio',
        blank=True,
    )

    role = models.CharField(
        'User role',
        max_length=15,
        choices=USER_ROLE,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.email


class Subscriptions(models.Model):

    """User subscription model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        models.UniqueConstraint(
            fields=('user', 'following'),
            name='unique_subscription_user'
        )
