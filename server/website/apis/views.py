from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from .dao import CategoryRepository, UserRepository, CourseRepository
from .serializers import UserSerializer, RegisterSerializer, CategorySerializer, CourseSerializer


class UserViewSet(viewsets.GenericViewSet, generics.CreateAPIView):
    queryset = UserRepository().get_all()
    serializer_class = RegisterSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

        return [permission() for permission in permission_classes]

    @csrf_exempt
    @action(detail=False, methods=["get"], url_path="current-user", name="Current User")
    def current_user(self, request):
        """Get the currently logged on user."""
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = CategoryRepository().get_all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = CourseRepository().get_all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
