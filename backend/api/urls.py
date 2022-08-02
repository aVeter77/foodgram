from django.urls import include, path
from rest_framework import routers

from .views import (
    CustomCurrentUser, CustomUserViewSet, IngredientViewSet, RecipeViewSet,
    TagViewSet,
)

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', CustomUserViewSet, basename='custom-user')

urlpatterns = [
    path('users/me/', CustomCurrentUser.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
