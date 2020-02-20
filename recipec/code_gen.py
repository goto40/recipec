from textx import generator, get_children_of_type
from os.path import dirname, abspath, join, splitext, basename, exists
import click


@generator('recipe-plan', 'md')
def plan_generator(metamodel, model, output_path, overwrite, debug, **custom_args):
    input_file = model._tx_filename
    base_dir = output_path if output_path else dirname(input_file)
    base_name, _ = splitext(basename(input_file))
    output_file = abspath(
        join(base_dir, "{}.{}".format(base_name, 'md')))
    if overwrite or not exists(output_file):
        click.echo('-> {}'.format(output_file))
        model_export(model, output_file)
    else:
        click.echo('-- Skipping: {}'.format(output_file))


def model_export(model, output_file):
    import jinja2
    plan = get_children_of_type("Plan",model)
    assert len(plan)==1
    plan=plan[0]

    all_ingredients = {} # ingredientType, count
    for e in get_children_of_type("PlanEntry",plan):
        for i in get_children_of_type("Ingredient",e.get_recipe()):
            all_ingredients[i.get_type()] = \
                all_ingredients.get(i.get_type(),0.0) \
                + i.get_count_in_default_units(float(e.person_count))
            #print("{} {}".format(i.get_type().name, all_ingredients[i.get_type()]))

    config = get_all(model, "Config")
    config=config[0]

    this_folder = dirname(abspath(__file__))
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(this_folder, "template")),
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja_env.get_template('plan.template')
    with open(output_file, 'w') as f:
        f.write(template.render(plan=plan, config=config,
                                all_ingredients=all_ingredients))


def get_all(model, what):
    lst=[]
    for m in model._tx_model_repository.all_models.filename_to_model.values():
        lst = lst + get_children_of_type(what, m)
    return lst
