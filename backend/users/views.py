from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import User
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import Subscriptions
from users.serializers import SubShowSerializer


class CustomUserViewSet(UserViewSet):

    """Customized user viewset."""
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)
        follow = Subscriptions.objects.filter(
            user=request.user,
            following=user
        )
        if request.method == 'POST':
            if user == request.user:
                error = {
                    'errors': 'Are you trying to subscribe to yourself.'
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            obj, created = Subscriptions.objects.get_or_create(
                user=request.user,
                following=user
            )
            if not created:
                error = {
                    'errors': 'You are already subscribed to this user.'
                }
                follow.delete()
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubShowSerializer(obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not follow.exists():
            error = {
                'errors': 'You were not subscribed to this user.'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
