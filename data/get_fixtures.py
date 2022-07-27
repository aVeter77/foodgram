import json


def get_json(name):
    with open(name, 'rb') as f:
        ingredients = json.load(f)
        units = [ingredient['measurement_unit'] for ingredient in ingredients]
    units = list(set(units))
    return ingredients, units


def main():
    ingredients_json, units = get_json('ingredients.json')

    ingredients = {
        ingredient['name']: units.index(ingredient['measurement_unit']) + 1
        for ingredient in ingredients_json
    }

    ing_fixtures = []
    i = 1
    for value, item in ingredients.items():
        fixt_dict = {
            'model': 'recipes.ingredient',
            'pk': i,
            'fields': {
                'name': value,
                'measurement_unit': item,
            },
        }
        ing_fixtures.append(fixt_dict)
        i += 1

    with open('fixtures_ingredients.json', 'w') as fp:
        json.dump(ing_fixtures, fp)

    units_fixtures = []
    i = 1
    for unit in units:
        fixt_dict = {
            'model': 'recipes.unit',
            'pk': i,
            'fields': {'name': unit},
        }
        units_fixtures.append(fixt_dict)
        i += 1

    with open('fixtures_units.json', 'w') as fp:
        json.dump(units_fixtures, fp)


if __name__ == '__main__':
    main()
