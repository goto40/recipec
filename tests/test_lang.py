from __future__ import unicode_literals
from textx import metamodel_for_language
from os.path import join, dirname, abspath
import pytest


def test_lang_config():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_for_language('recipe-config')
    model = mm.model_from_file(join(
        this_folder, 'demos', 'config', 'settings.config'))
    assert model is not None
    assert model.name == 'german'


def test_lang_ingredient():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_for_language('recipe-ingredient')
    model = mm.model_from_file(join(
        this_folder, 'demos', 'ingredients', 'obst.ingredient'))
    assert model is not None
    assert len(model.ingredientTypes) == 2
    assert model.ingredientTypes[0].name == 'Bananen'
    assert model.ingredientTypes[1].name == 'Banane'


def test_lang_recipe():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_for_language('recipe-recipe')
    model = mm.model_from_file(join(
        this_folder, 'demos', 'schinken-bananen.recipe'))
    assert model is not None
    assert model.recipe.title == "Schinken Bananen"
    assert len(model.recipe.ingredients) == 4
    assert model.recipe.person_count == pytest.approx(2)
    assert model.recipe.ingredients[0].count == pytest.approx(4)
    assert model.recipe.ingredients[0].get_count_in_default_units(model.recipe.person_count) == pytest.approx(4*(150/4))
    assert model.recipe.ingredients[2].get_count_in_default_units(model.recipe.person_count) == pytest.approx(50)


def test_lang_plan():
    this_folder = dirname(abspath(__file__))
    mm = metamodel_for_language('recipe-plan')
    model = mm.model_from_file(join(
        this_folder, 'demos', 'bananentag.plan'))
    assert model is not None
