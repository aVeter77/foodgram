# Generated by Django 3.2.14 on 2022-07-30 23:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'ordering': ['recipe'], 'verbose_name': 'Ингредиенты для рецепта', 'verbose_name_plural': 'Ингредиенты для рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепты', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время, мин'),
        ),
    ]
