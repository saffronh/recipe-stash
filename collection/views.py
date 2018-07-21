from django.shortcuts import render, redirect
from collection.models import Recipe
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
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe,})

@login_required
def edit_recipe(request, slug):
    recipe = Recipe.objects.get(slug=slug)

    #make sure logged-in user is owner of recipe
    if recipe.user != request.user:
        raise Http404

    # set form to be used
    form_class = RecipeForm
    # if we are coming to this from a submitted form
    if request.method == 'POST':
        form = form_class(data=request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', slug=recipe.slug)
    # else just create form
    else:
        form = form_class(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {
        'recipe': recipe,
        'form': form,
    })

def create_recipe(request):
    form_class = RecipeForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.slug = slugify(recipe.name)

            recipe.save()

            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = form_class()

    return render(request, 'recipes/create_recipe.html', {'form': form,})

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
