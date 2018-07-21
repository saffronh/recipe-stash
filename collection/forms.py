from django.forms import ModelForm

from collection.models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description',)
