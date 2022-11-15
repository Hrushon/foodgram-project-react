from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.paginators import CustomPagination
from .serializers import SubscriptionCreateSerializer, SubscriptionSerializer

User = get_user_model()


class UserCustomViewSet(UserViewSet):
    """Кастомизированный вьюсет библиотеки 'djoser'."""

    pagination_class = CustomPagination

    @action(
        methods=['get'], detail=False,
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        user = self.request.user

        def queryset():
            return User.objects.filter(subscriber__user=user)

        self.get_queryset = queryset
        return self.list(request)

    @action(
        methods=['post', 'delete'], detail=True,
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id):
        user = self.request.user
        author = self.get_object()
        if request.method == 'DELETE':
            instance = user.following.filter(author=author)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Вы не подписаны на этого автора.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'author': id
        }
        subscription = SubscriptionCreateSerializer(data=data)
        subscription.is_valid(raise_exception=True)
        subscription.save()
        serializer = self.get_serializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
