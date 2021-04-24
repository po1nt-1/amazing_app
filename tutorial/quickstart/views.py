from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from tutorial.quickstart.models import Tweet, Follow
from tutorial.quickstart.permissions import IsTweetAuthorOrReadOnly
from tutorial.quickstart.serializers import (
    FollowSerializer,
    TweetSerializer,
    UserSerializer,
    UserFollowsSerializer,
    UserFollowedSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows tweets to be viewed or edited.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsTweetAuthorOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UserTweetsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows tweets to be listed.
    """
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FollowViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet
):
    """
    API endpoint that allows Follow to be post and delete.
    """

    queryset = Follow.objects
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follows = User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(follower=self.request.user, follows=follows)

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field]
        )


class FeedViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    API endpoint that allows tweets to be viewed or edited.
    """
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            author__followers__follower=self.request.user
        )


class UserFollowsViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Follow.objects
    serializer_class = UserFollowsSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follower__username=username)


class UserFollowedViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Follow.objects
    serializer_class = UserFollowedSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follows__username=username)
