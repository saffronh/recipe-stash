from django.shortcuts import render, redirect
from django.forms import ModelForm, modelformset_factory
from collection.models import Recipe, Ingredient, Method, Tags
from collection.forms import RecipeForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    recipes = Recipe.objects.all().order_by('name')
    return render(request, 'index.html', {
        'recipes': recipes,
      })

def recipe_detail(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    ingredients = Ingredient.objects.filter(recipe_id=recipe.id)
    methods = Method.objects.filter(recipe_id=recipe.id).order_by('id')
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'methods': methods,})

@login_required
def edit_recipe(request, slug):
    recipe = Recipe.objects.get(slug=slug)

    #make sure logged-in user is owner of recipe
    if recipe.user != request.user:
        raise Http404

    # set forms to be used
    recipe_form = RecipeForm
    ingredient_formset = modelformset_factory(Ingredient, fields=('ingredient_name', 'quantity', 'measure',))
    method_formset = modelformset_factory(Method, fields=('description',))

    # if we are coming to this from a submitted form
    if request.method == 'POST':
        recipeform = recipe_form(data=request.POST, instance=recipe)
        ingredientform = ingredient_formset(request.POST, queryset=Ingredient.objects.filter(recipe_id=recipe.id))
        methodform = method_formset(request.POST, queryset=Method.objects.filter(recipe_id=recipe.id))
        if recipeform.is_valid() and ingredientform.is_valid() and methodform.is_valid():
            recipeform.save()

            # link ingredients to recipe
            ingredients = ingredientform.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe

            # link methods to recipe
            methods = methodform.save(commit=False)
            for method in methods:
                method.recipe = recipe

            ingredientform.save()
            methodform.save()

            return redirect('recipe_detail', slug=recipe.slug)
    # else just create form
    else:
        recipeform = recipe_form(instance=recipe)
        ingredientform = ingredient_formset(queryset=Ingredient.objects.filter(recipe_id=recipe.id))
        methodform = method_formset(queryset=Method.objects.filter(recipe_id=recipe.id))
    return render(request, 'recipes/edit_recipe.html', {
        'recipe': recipe,
        'recipeform': recipeform,
        'ingredientform': ingredientform,
        'methodform': methodform,
    })

def create_recipe(request):
    recipe_form = RecipeForm
    ingredient_formset = modelformset_factory(Ingredient, extra=10, fields=('ingredient_name', 'measure', 'quantity',))
    method_formset = modelformset_factory(Method, extra=10, fields=('description',))

    if request.method == 'POST':
        recipeform = recipe_form(request.POST)
        ingredientform = ingredient_formset(request.POST, queryset=Ingredient.objects.none())
        methodform = method_formset(request.POST, queryset=Method.objects.none())
        if recipeform.is_valid() and ingredientform.is_valid() and methodform.is_valid():
            recipe = recipeform.save(commit=False)
            recipe.user = request.user
            recipe.slug = slugify(recipe.name)

            recipe.save()

            # link ingredients to recipe
            ingredients = ingredientform.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe

            # link methods to recipe
            methods = methodform.save(commit=False)
            for method in methods:
                    method.recipe = recipe

            ingredientform.save()
            methodform.save()

            return redirect('recipe_detail', slug=recipe.slug)
    else:
        recipeform = recipe_form()
        ingredientform = ingredient_formset(queryset=Ingredient.objects.none())
        methodform = method_formset(queryset=Method.objects.none())

    return render(request, 'recipes/create_recipe.html', {
        'recipeform': recipeform,
        'ingredientform': ingredientform,
        'methodform': methodform,})

def browse_by_name(request, initial=None):
    if initial:
        recipes = Recipe.objects.filter(name__istartswith=initial)
        recipes = recipes.order_by('name')
    else:
        recipes = Recipe.objects.all().order_by('name')
    return render(request, 'browse/browse.html', {
        'recipes': recipes,
        'initial': initial,
        })

def delete_recipe(request, recipe_id):
    Ingredient.objects.filter(recipe_id=recipe_id).delete()
    Method.objects.filter(recipe_id=recipe_id).delete()
    Recipe.objects.filter(id=recipe_id).delete()
    return redirect('home')
