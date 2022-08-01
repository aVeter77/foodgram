from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Unit(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)

    class Meta:
        verbose_name = 'Ед. измерения'
        verbose_name_plural = 'Ед. измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    measurement_unit = models.ForeignKey(
        Unit,
        verbose_name='Ед. измерения',
        on_delete=models.PROTECT,
        related_name='units',
    )

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredientrecipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredientrecipe_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Ингредиенты для рецептов'
        verbose_name_plural = 'Ингредиенты для рецептов'

    def __str__(self):
        return f'{self.recipe}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=50, unique=True
    )
    color = models.CharField(
        verbose_name='Цвет', max_length=7, default='#CCCCCC', unique=True
    )
    slug = models.SlugField(verbose_name='Псевдоним', unique=True)

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tagrecipe_tag',
        verbose_name='Тэг',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='tagrecipe_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Тэги для рецептов'
        verbose_name_plural = 'Тэги для рецептов'

    def __str__(self):
        return f'{self.tag}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through=TagRecipe,
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientRecipe,
        verbose_name='Ингридиенты',
        related_name='recipes_ingredients',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(verbose_name='Картинка', upload_to='recipes/')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время, мин',
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'], name='unique_name_author'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'

    @property
    def tags_list(self):
        return list(self.tags.values_list('name', flat=True))

    @property
    def ingredients_list(self):
        return list(
            self.ingredients.values_list(
                'name',
                'ingredientrecipe_ingredients__amount',
                'measurement_unit__name',
            )
        )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='unique subscription'
            )
        ]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        app_label = 'users'


class ShoppingСart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique shopping cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        app_label = 'users'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique favotite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        app_label = 'users'
