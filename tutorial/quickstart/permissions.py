

from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, tweet):
        return bool(
            request.method in SAFE_METHODS or
            tweet.author == request.user
        )
