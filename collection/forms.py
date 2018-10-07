from django.forms import ModelForm
#from djangoformsetjs.utils import formset_media_js

from collection.models import Recipe, Ingredient, Method, Tags

# form for entering basic info about each recipe
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name',) # excluded 'tags' for now

# form for each ingredient
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ('ingredient_name', 'quantity', 'measure', )

    #class Media(object):
    #  js = formset_media_js

# form for each method
class MethodForm(ModelForm):
    class Meta:
        model = Method
        fields = ('description',)
