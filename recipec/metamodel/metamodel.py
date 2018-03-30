from __future__ import unicode_literals
from os.path import dirname, abspath
from textx import metamodel_from_file, get_model, get_children_of_type
import os
from textx.scoping import MetaModelProvider, GlobalModelRepository
import textx.scoping.providers as scoping_providers
import glob
from recipec.metamodel.mm_classes import IngredientTypeDef, Ingredient, \
    IngredientAlias

def get_model_repo(args):

    global_repo = GlobalModelRepository()
    global_repo_provider = scoping_providers.PlainNameGlobalRepo(
        glob_args={"recursive": True})
    global_repo_provider.register_models(args.in_folder+"/**/*.recipe")
    global_repo_provider.register_models(args.in_folder+"/**/*.ingredient")
    global_repo_provider.register_models(args.in_folder+"/**/*.config")
    #global_repo_provider.register_models(args.in_folder+"/**/*.plan")

    r_mm = _get_meta_model(
        global_repo_provider, global_repo, '../grammar/Recipe.tx')
    i_mm = _get_meta_model(
        global_repo_provider, global_repo, '../grammar/Ingredient.tx')
    c_mm = _get_meta_model(
        global_repo_provider, global_repo, '../grammar/Config.tx')
    p_mm = _get_meta_model(
        global_repo_provider, global_repo, '../grammar/Plan.tx')

    MetaModelProvider.add_metamodel("*.recipe", r_mm)
    MetaModelProvider.add_metamodel("*.ingredient", i_mm)
    MetaModelProvider.add_metamodel("*.config", c_mm)
    MetaModelProvider.add_metamodel("*.plan", p_mm)

    return global_repo_provider.load_models_in_model_repo().all_models, p_mm


def _get_meta_model(global_repo_provider, global_repo, grammar_file_name, debug=False, **kwargs):

    def recipe_scope_provider(obj, attr, obj_ref):
        f2m = get_model(obj)._tx_model_repository.all_models.filename_to_model
        filenames = f2m.keys()
        res = list(filter(
            lambda fn: (obj_ref.obj_name in fn)
                      and (len(get_children_of_type("Recipe",f2m[fn]))==1),
            filenames))
        if len(res)==1:
            return get_children_of_type("Recipe",f2m[res[0]])[0]
        else:
            return None

    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(os.path.join(this_folder, grammar_file_name),
                             debug=debug, classes=[IngredientTypeDef, Ingredient, IngredientAlias],
                             global_repository=global_repo)
    mm.register_scope_providers({
            "*.*": global_repo_provider,
            "Ingredient.unit": scoping_providers.ExtRelativeName("type","units","extends"),
            "PlanEntry.recipe": recipe_scope_provider
    })
    return mm
