from __future__ import unicode_literals
from textx import language
from os.path import dirname, abspath, join
from textx import metamodel_from_file
import textx.scoping.providers as scoping_providers


from recipec.mm_classes import IngredientTypeDef, Ingredient, \
    IngredientAlias

@language('recipe-config', '*.config')
def config_lang():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(join(this_folder, "grammar", "Config.tx"))
    return mm


@language('recipe-ingredient', '*.ingredient')
def ingredient_lang():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(join(this_folder, "grammar", "Ingredient.tx"),
                             classes=[IngredientTypeDef, IngredientAlias])
    return mm


@language('recipe-recipe', '*.recipe')
def recipe_lang():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(join(this_folder, "grammar", "Recipe.tx"),
                             classes=[Ingredient])
    config_provider = scoping_providers.PlainNameGlobalRepo(
        "**/*.config", glob_args={"recursive": True})
    ingredient_type_provider = scoping_providers.PlainNameGlobalRepo(
        "**/*.ingredient", glob_args={"recursive": True})
    mm.register_scope_providers({
        "Recipe.persons": config_provider,
        "Ingredient.type": ingredient_type_provider,
        "Ingredient.unit": scoping_providers.ExtRelativeName("type", "units", "extends"),
    })
    return mm


@language('recipe-plan', '*.plan')
def plan_lang():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(join(this_folder, "grammar", "Plan.tx"),
                             classes=[Ingredient])
    mm.register_scope_providers({
        "*.*": scoping_providers.PlainNameImportURI()  # each import is a recipe model
    })
    return mm
