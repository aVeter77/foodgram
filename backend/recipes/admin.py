from django.contrib.admin import ModelAdmin, display, register, site
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter,
)

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe, Unit

site.register(Unit)
site.register(Tag)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ("id", "name", "measurement_unit")
    list_editable = ("measurement_unit",)
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = (("name", DropdownFilter),)
    empty_value_display = "-пусто-"


@register(IngredientRecipe)
class IngredientRecipeAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ("id", "recipe")
    list_display_links = ("id", "recipe")
    search_fields = ("recipe__name",)
    list_filter = (("recipe__name", DropdownFilter),)
    empty_value_display = "-пусто-"


@register(TagRecipe)
class TagRecipeAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ("id", "recipe")
    list_display_links = ("id", "recipe")
    search_fields = ("recipe__name",)
    list_filter = (("recipe__name", DropdownFilter),)
    empty_value_display = "-пусто-"


@register(Recipe)
class RecipeAdmin(ModelAdmin):

    list_per_page = 10
    list_display = (
        "id",
        "name",
        "author",
    )
    list_display_links = ("id", "name", "author")
    search_fields = ("name",)
    list_filter = (
        ("author", RelatedDropdownFilter),
        ("name", DropdownFilter),
        ("tags", RelatedDropdownFilter),
    )
    readonly_fields = ("get_ingredients", "get_tags", "get_favorites")
    empty_value_display = "-пусто-"

    @display(description="Теги")
    def get_tags(self, obj):
        if obj.tags_list:
            return "\n".join(obj.tags_list)
        return "-пусто-"

    @display(description="В избранном")
    def get_favorites(self, obj):
        if obj.favorite.count():
            return obj.favorite.count()
        return "0"

    @display(description="Ингредиенты")
    def get_ingredients(self, obj):
        if obj.ingredients_list:
            return "\n".join(
                [
                    " ".join([str(value) for value in ingredient])
                    for ingredient in obj.ingredients_list
                ]
            )
        return "0"
