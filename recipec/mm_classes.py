class ModelItemBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

class IngredientTypeDef(ModelItemBase):
    def __init__(self, **kwargs):
        super(IngredientTypeDef, self).__init__()
        self._init_xtextobj(**kwargs)
        #print("ingredient: {}".format(self.name))

    def get_default_unit(self):
        return self.get_all_units()[0]

    def get_all_units(self):
        if self.extends!=None:
            return self.units+self.extends.get_all_units()
        else:
            return self.units

class IngredientAlias(ModelItemBase):
    def __init__(self, **kwargs):
        super(IngredientAlias, self).__init__()
        self._init_xtextobj(**kwargs)
        self.units=[]

    def get_default_unit(self):
        return self.extends.get_default_unit()

    def get_all_units(self):
        return self.extends.get_all_units()


class Ingredient(ModelItemBase):
    def __init__(self, **kwargs):
        super(Ingredient, self).__init__()
        self._init_xtextobj(**kwargs)

    def to_str(self, nb_persons=1):
        nb_persons = float(nb_persons)
        count, unit_name, type_name =  float(self.count), self.unit.name, self.type.name
        count_recipe = float(self.parent.person_count)
        count = count/count_recipe*nb_persons
        unit0 = self.type.get_default_unit()
        if (self.unit == unit0 or self.unit.weight==unit0.weight):
            return "{} {} {}".format(count, unit_name, type_name);
        else:
            count0 = self.get_count_in_default_units(nb_persons)
            return "{} {} {} ({} {})".format(
                count, unit_name, type_name,
                count0, unit0.name
            );

    def get_type(self):
        t = self.type
        while t.__class__.__name__ == "IngredientAlias":
            t=t.extends
        return t

    def get_count_in_default_units(self,nb_persons=1):
        count_recipe = float(self.parent.person_count)
        count, unit_name, type_name =  float(self.count), self.unit.name, self.type.name
        count = count/count_recipe*nb_persons
        unit0 = self.type.get_default_unit()
        is_count_ref = float(self.unit.weight)
        should_count_ref = float(unit0.weight)
        return count / is_count_ref * should_count_ref


class PlanEntry(ModelItemBase):
    def __init__(self, **kwargs):
        super(PlanEntry, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_recipe(self):
        assert len(self._tx_loaded_models)==1, "no wildcards for recipes supported"
        recipe = self._tx_loaded_models[0].recipe
        return recipe
