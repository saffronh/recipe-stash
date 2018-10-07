from django.contrib import admin

# Import models
from collection.models import Recipe, Ingredient, Method, Tags

# Set up automated slug creation
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}

# formset for editing all ingredients/methods
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}

# Register models
admin.site.register(Recipe, RecipeAdmin)
