from django.contrib.admin import ModelAdmin, register
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter,
)
from recipes.models import Favorite, ShoppingСart, Subscription

from .models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username', 'email')
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        (
            'username',
            DropdownFilter,
        ),
        (
            'email',
            DropdownFilter,
        ),
    )
    empty_value_display = '-пусто-'


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'author', 'user')
    list_display_links = ('id', 'author', 'user')
    search_fields = ('author', 'user')
    list_filter = (
        (
            'author',
            RelatedDropdownFilter,
        ),
        (
            'user',
            RelatedDropdownFilter,
        ),
    )
    empty_value_display = '-пусто-'


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'recipe', 'user')
    list_display_links = ('id', 'recipe', 'user')
    search_fields = ('recipe',)
    list_filter = (
        (
            'recipe',
            RelatedDropdownFilter,
        ),
        (
            'user',
            RelatedDropdownFilter,
        ),
    )
    empty_value_display = '-пусто-'


@register(ShoppingСart)
class ShoppingСartAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ('id', 'recipe', 'user')
    list_display_links = ('id', 'recipe', 'user')
    search_fields = ('recipe',)
    list_filter = (
        (
            'recipe',
            RelatedDropdownFilter,
        ),
        (
            'user',
            RelatedDropdownFilter,
        ),
    )
    empty_value_display = '-пусто-'
