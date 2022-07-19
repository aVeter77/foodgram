from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe, Tag, User
from rest_framework import serializers


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

        read_only_fields = [
            'id',
        ]


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Recipe

        read_only_fields = ('author',)
