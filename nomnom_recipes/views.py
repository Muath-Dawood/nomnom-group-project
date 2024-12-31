from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from django.db import IntegrityError
from django.contrib import messages

from .models import Recipe
User = get_user_model()

def index(req):
    return render(req,'recipes/home.html')

def my_recipes(req):
  if req.user.is_authenticated:
    recipes = Recipe.objects.filter(user=req.user.id)
    return render(req, 'recipes/my_recipes.html', {'recipes': recipes})
  else:
    return redirect('/')

def add_recipe(req):
  if req.user.is_authenticated:
    post_data = {
      'title': req.POST['title'],
      'description': req.POST['description'],
      'ingredients': req.POST['ingredients'],
      'instructions': req.POST['instructions'],
      'image': req.FILES['image'] 
    }
    user = User.objects.get(id=req.user.id)
    errors = Recipe.objects.validate_recipe_data(post_data)
    if len(errors):
        for value in errors.values():
            messages.error(req, value)
        return redirect('/add_recipe')    
    new_recipe = Recipe(created_by=user, **post_data)
    new_recipe.save()
    return redirect(f'/recipe/{new_recipe.id}')

def delete_recipe(req, id):
  recipe = Recipe.objects.get(id=id)
  if req.user.is_authenticated:
    if recipe.user.id != req.user.id:
        messages.error(req, "YOU CAN NOT DELETE A RECIPE THAT IS NOT YOURS!")
        return redirect('/my_recipes')
    recipe = Recipe.objects.get(id=id)
    recipe.delete()
  return redirect('/my_recipes')

def show_recipe(req, id):
  if req.user.is_authenticated:
    recipe = Recipe.objects.get(id=id)
    return render(req, 'recipe/show_recipe.html', {'recipe': recipe})
  else:
    return redirect('/auth/login')

def edit_recipe(req, id):
    recipe = Recipe.objects.get(id=id)
    if req.user.is_authenticated:
        if recipe.user.id != req.user.id:
            messages.error(req, "YOU CAN NOT EDIT A RECIPE THAT IS NOT YOURS!")
        return redirect('/my_recipes')
    if req.method == 'GET':
        context = {
        'recipe': recipe.objects.get(id=id)
        }
        return render(req, 'recipe/edit_recipe.html', context)
    
    if req.method == 'POST':
        post_data = {
            'title': req.POST['title'],
            'description': req.POST['description'],
            'ingredients': req.POST['ingredients'],
            'instructions': req.POST['instructions'],
            'image': req.FILES['image']
        }
        errors = Recipe.objects.validate_recipe_data(post_data)
        if len(errors):
            for value in errors.values():
                messages.error(req, value)
            return redirect('/edit_recipe')
        for attr in post_data:
            if hasattr(recipe, attr):
                setattr(recipe, attr, post_data[attr])
        recipe.save()
        return redirect(f'/recipes/{recipe.id}')
    else:
        return redirect('/auth/login')