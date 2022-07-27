from recipes.models import Recipe, Tag, User
from rest_framework import exceptions, generics, permissions, viewsets

from .serializers import (
    CustomUserSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CustomCurrentUserViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return RecipeWriteSerializer
        elif self.request.method == 'PATCH':
            raise exceptions.ValidationError('Метод PATCH не разрешен.')
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        return self.perform_create
