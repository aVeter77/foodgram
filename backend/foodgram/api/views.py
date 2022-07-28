from djoser.views import UserViewSet
from recipes.models import (
    Favorite,
    Recipe,
    Shopping_cart,
    Subscription,
    Tag,
    User,
)
from rest_framework import exceptions, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    CustomUserSerializer,
    RecipeInListSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    SubscribeSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = self.get_object()
        if request.method == 'POST':
            serializer = SubscribeSerializer(author)
            Subscription.objects.update_or_create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Subscription.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomCurrentUser(generics.RetrieveAPIView):
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

    def recipe_in_list(self, request, recipe_model):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'POST':
            serializer = RecipeInListSerializer(
                recipe, context={"request": request}
            )
            recipe_model.objects.update_or_create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        recipe_model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self.recipe_in_list(request, Favorite)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return self.recipe_in_list(request, Shopping_cart)
