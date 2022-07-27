from django.urls import include, path
from rest_framework import routers

from .views import CustomCurrentUserViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'users/me/', CustomCurrentUserViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
