from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from django.db import IntegrityError
from django.contrib import messages

from .models import Recipe
User = get_user_model()

def add_recipe(req):
  if req.user.is_authenticated:
    post_data = {
      'title': req.POST['title'],
      'description': req.POST['description'],
      'ingredients': req.POST['ingredients'],
      'instructions': req.POST['instructions'],
      'image': req.POST['image']
    #   'image': req.FILES['image'] // is this the right code line for images ?? 
    }
    user = User.objects.get(id=req.user.id)
    errors = Recipe.objects.validate_recipe_data(post_data)
    try:
      if len(errors):
        for value in errors.values():
          messages.error(req, value)
        raise ValueError("Messing form fields!")
      new_show = Recipe(user=user, **post_data)
      new_show.save()
    except IntegrityError:
      messages.error(req, "Name already exists!")
      return redirect('/add_recipe')
    except ValueError:
      return redirect('/add_recipe')
    else:
      return redirect('/add_recipe')
  else:
    return redirect('/accounts/signin')

def delete_recipe(req, id):
  Recipe = Recipe.objects.get(id=id)
  if req.user.is_authenticated:
    if Recipe.user.id != req.user.id:
        messages.error(req, "YOU CAN NOT DELETE A RECIPE THAT IS NOT YOURS!")
        return redirect('/add_recipe')
    Recipe = Recipe.objects.get(id=id)
    Recipe.delete()
  return redirect('/add_recipe')