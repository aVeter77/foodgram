from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Unit(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    measurement_unit = models.ForeignKey(
        Unit,
        verbose_name='Ед. измерения',
        on_delete=models.PROTECT,
        related_name='units',
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=50, unique=True
    )
    color = models.CharField(
        verbose_name='Цвет', max_length=6, default='cccccc', unique=True
    )
    slug = models.SlugField(verbose_name='Псевдоним', unique=True)

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


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
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(verbose_name='Картинка', upload_to='recipes/')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин',
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Подписки',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчики',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='unique subscription'
            )
        ]


class Shopping_cart(models.Model):
    purchase = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Покупки',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепты',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'purchase'], name='unique purchase'
            )
        ]


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
        verbose_name='Избранные',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique favotite'
            )
        ]
