#from os.path import expanduser
import recipec.metamodel.metamodel as metamodel
from textx import get_children_of_type, get_model
from os.path import abspath,dirname

def recipec(develop=False):
    try:
        import argparse
        parser = argparse.ArgumentParser(description='recipe console')
        parser.add_argument('--in-folder', dest='in_folder', default=".", type=str,
                            help='folder where to generate the code')
        parser.add_argument('-r', '--list-recipes', dest='list_recipes', default=False,
                            action='store_true', help='show list of recipes')
        parser.add_argument('-i', '--list-ingredients', dest='list_ingredients', default=False,
                            action='store_true', help='show list of ingredients')
        parser.add_argument('-p', '--plan', dest='eval_plan', type=str, default=None,
                            help='show list of ingredients')
        parser.add_argument('-o', '--outfile', dest='out_file', type=str, default="output.md",
                            help='output file')
        parser.add_argument('-x', '--export', dest='export_model', default=False,
                            action='store_true', help='export recipes and ingredients')
        parser.add_argument('--export-model-file', dest='export_model_file', type=str, default="recipes_and_ingredients.dot",
                            help='export model file name')

        args = parser.parse_args()

        model_repo, p_mm = metamodel.get_model_repo(args)

        if args.list_ingredients:
            show_list_of_ingredients(model_repo)

        if args.list_recipes:
            show_list_of_recipes(model_repo)

        if args.eval_plan:
            eval_plan(p_mm, model_repo, args.eval_plan, args.out_file)

        if args.export_model:
            from textx.export import model_export
            model_export(None, args.export_model_file, model_repo)

    except Exception as e:
        print(e)
        if develop:
            raise e

def eval_plan(p_mm, model_repo, plan_fn, out_file):
    import jinja2
    m = p_mm.model_from_file(plan_fn)
    plan = get_children_of_type("Plan",m)
    assert len(plan)==1
    plan=plan[0]

    all_ingredients = {} # ingredientType, count
    for e in get_children_of_type("PlanEntry",plan):
        for i in get_children_of_type("Ingredient",e.recipe):
            all_ingredients[i.get_type()] = \
                all_ingredients.get(i.get_type(),0.0) \
                + i.get_count_in_default_units(float(e.person_count))
            #print("{} {}".format(i.get_type().name, all_ingredients[i.get_type()]))

    config = get_all(model_repo, "Config")
    config=config[0]

    this_folder = dirname(abspath(__file__))
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/template"),
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja_env.get_template('plan.template')
    with open(out_file, 'w') as f:
        f.write(template.render(plan=plan, config=config,
                                all_ingredients=all_ingredients))


def get_all(model_repo, what):
    lst=[]
    for m in model_repo.filename_to_model.values():
        lst = lst + get_children_of_type(what, m)
    return lst

def show_list_of_ingredients(model_repo):
    for i in get_all(model_repo,what="IngredientTypeDef"):
        print("{:<30}: {:<30} from {}".format(
            i.name,
            ','.join([u.name for u in i.get_all_units()]),
            get_model(i)._tx_filename
        ))
    for i in get_all(model_repo,what="IngredientAlias"):
        print("{:<30}= {:<30} from {}".format(
            i.name,
            i.extends.name,
            get_model(i)._tx_filename
        ))

def show_list_of_recipes(model_repo):
    for r in get_all(model_repo,what="Recipe"):
        print("{}, {}".format(
            r.title,
            get_model(r)._tx_filename
        ))
        for i in r.ingredients:
            print("{}".format(i.to_str()))
        print(r.description)


if __name__=="__main__":
    recipec(develop=True)
