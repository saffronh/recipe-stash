from django.contrib import admin

# Import models
from collection.models import Recipe

# Set up automated slug creation
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}

# Register models
admin.site.register(Recipe, RecipeAdmin)
