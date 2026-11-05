from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserMeSerializer


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    """Read and edit only the profile owned by the current session user."""

    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user
