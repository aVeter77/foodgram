from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from paginators import CustomPaginator
from recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingСart, Subscription, Tag, User,
)
from rest_framework import (
    exceptions, filters, generics, permissions, status, viewsets,
)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import RecipeFilter
from .permissions import AuthorOrReadOnly
from .serializers import (
    CustomUserSerializer, IngredientReadSerializer, RecipeInListSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, SubscribeSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = self.get_object()
        if user == author:
            raise exceptions.ValidationError(
                'На самого себя подписаться нельзя.'
            )
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author, context={"request": request}
            )
            Subscription.objects.update_or_create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Subscription.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request, pk=None):
        user = self.request.user
        authors = User.objects.filter(subscriber__user=user)
        page = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class CustomCurrentUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(pk=self.request.user.id)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST']:
            return RecipeWriteSerializer
        elif self.request.method == 'PUT':
            raise exceptions.ValidationError('Метод PUT не разрешен.')
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
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        return self.recipe_in_list(request, Favorite)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        return self.recipe_in_list(request, ShoppingСart)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request, pk=None):
        user = request.user
        recipes = Recipe.objects.filter(recipe__user=user)
        name = 'ingredients__name'
        unit = 'ingredients__measurement_unit__name'
        amount = 'ingredientrecipe_recipes__amount'
        total = 'total'
        ingredients = (
            recipes.values(name, unit)
            .order_by(name)
            .annotate(total=Sum(amount))
        )
        data = [
            f'{item.get(name)} - {item.get(total)} {item.get(unit)}'
            for item in ingredients
        ]
        return HttpResponse('\n'.join(data), content_type='text/plain')
