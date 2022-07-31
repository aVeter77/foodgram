from django.contrib.admin import ModelAdmin, display, register, site
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
)
from recipes.models import Favorite, Shopping_cart, Subscription

from .models import User

site.register(User)


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
