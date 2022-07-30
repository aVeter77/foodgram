from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Shopping_cart,
    Subscription,
    Tag,
    TagRecipe,
    User,
)
from rest_framework import exceptions, serializers


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

        read_only_fields = ('id',)


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                author=obj.id, user=user
            ).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AuthorRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FilteredRecipeInListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        if recipes_limit and recipes_limit.isdigit():
            data = data.all()[: int(recipes_limit)]
        return super(FilteredRecipeInListSerializer, self).to_representation(
            data
        )


class RecipeInListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilteredRecipeInListSerializer
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipeWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = '__all__'

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name', 'author'),
                message='Рецепт с таким названием уже существует.',
            )
        ]

    def validate_ingredients(self, value):
        ingredients_id = [ingredient.get('id') for ingredient in value]
        if len(ingredients_id) != len(list(set(ingredients_id))):
            raise exceptions.ValidationError(
                'Ингредиенты не должны повторяться'
            )
        elif len(ingredients_id) == 0:
            raise exceptions.ValidationError(
                'В рецепте должны быть ингредиенты'
            )
        for id in ingredients_id:
            if not Ingredient.objects.filter(pk=id).exists():
                raise exceptions.ValidationError(
                    'Такой ингредиент не существует'
                )

        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            obj = Ingredient.objects.get(pk=id)
            IngredientRecipe.objects.create(
                ingredient=obj, amount=amount, recipe=recipe
            )

        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance.tags.clear()
        instance.ingredients.clear()

        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            obj = Ingredient.objects.get(pk=id)
            instance.ingredients.add(obj, through_defaults={'amount': amount})

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.tags.add(*tags)
        instance.save()

        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


class RecipeReadSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeReadSerializer(
        many=True, read_only=True, source='ingredientrecipe_recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(recipe=obj.id, user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Shopping_cart.objects.filter(
                recipe=obj.id, user=user
            ).exists()
        return False


class SubscribeSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeInListSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                author=obj.id, user=user
            ).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.recipes.count()
