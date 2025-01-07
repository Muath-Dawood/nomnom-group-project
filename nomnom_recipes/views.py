from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template.defaulttags import register
from .models import Recipe
from .models import Review
import json

User = get_user_model()

def search(req):
    recipes = Recipe.objects.filter(title__icontains = req.POST['search'])
    return render(req, 'recipes/search_results.html', {'recipes':recipes})

@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

def index(req):
    return render(req,'recipes/home.html')

def my_profile(req):
    return render(req, 'recipes/my_profile.html')

def contact(req):
    return render(req, 'recipes/contact_us.html')

def about_us(req):
    return render(req, 'recipes/about_us.html')

def my_recipes(req):
  if req.user.is_authenticated:
    current_user = User.objects.get(id=req.user.id)
    recipes = Recipe.objects.filter(created_by=current_user)
    return render(req, 'recipes/my_recipes.html', {'recipes': recipes})
  else:
    return redirect('/')

def all_recipes(req):
    recipes = Recipe.objects.all()
    return render(req, 'recipes/all_recipes.html', {'recipes': recipes})

def add_recipe(req):
  if req.user.is_authenticated:
    if req.method == "GET":
      return render(req,'recipes/add_recipe.html')
    else:
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
          return redirect('/recipes/add')
      new_recipe = Recipe(created_by=user, **post_data)
      new_recipe.save()
      return redirect('/my_recipes')
  else:
    return redirect('/auth/login')

def delete_recipe(req, id):
  recipe = Recipe.objects.get(id=id)
  if req.user.is_authenticated:
    if recipe.created_by.id != req.user.id:
        messages.error(req, "YOU CAN NOT DELETE A RECIPE THAT IS NOT YOURS!")
        return redirect('/my_recipes')
    recipe.delete()
    return redirect('/my_recipes')
  else:
    return redirect('/auth/login')

def show_recipe(req, id):
    recipe = Recipe.objects.get(id=id)
    reviews = recipe.reviews.all()
    average_rating = recipe.average_rating()
    return render(req, 'recipes/show_recipe.html', {'recipe': recipe, 'reviews': reviews, "average_rating": average_rating})

def edit_recipe(req, id):
    recipe = Recipe.objects.get(id=id)
    if req.user.is_authenticated:
        if recipe.created_by.id != req.user.id:
            messages.error(req, "YOU CAN NOT EDIT A RECIPE THAT IS NOT YOURS!")
            return redirect('/my_recipes')
        if req.method == 'GET':
            context = {
            'recipe': Recipe.objects.get(id=id)
            }
            return render(req, 'recipes/edit_recipe.html', context)

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
                return redirect(f'recipes/{recipe.id}/edit')
            for attr in post_data:
                if hasattr(recipe, attr):
                    setattr(recipe, attr, post_data[attr])
            recipe.save()
            return redirect(f'/recipes/{recipe.id}')
    else:
        return redirect('/auth/login')

def add_review(req, id):
    if req.user.is_authenticated:
        recipe = Recipe.objects.get(id=id)
        user = User.objects.get(id=req.user.id)
        post_data = {
            'rating': req.POST['rating'],
            'comment': req.POST['comment'],
        }
        errors = Review.objects.validate_review_data(post_data)
        if errors:
            for value in errors.values():
                messages.error(req, value)
            return redirect(f'/recipes/{recipe.id}')
        new_review = Review.objects.create(
            recipe=recipe,
            reviewer=user,
            rating=post_data['rating'],
            comment=post_data['comment']
        )
        new_review.save()
        messages.success(req, "Your review has been added successfully.")
        return redirect(f'/recipes/{recipe.id}')
    else:
        return redirect('/auth/login')

def edit_review(req,recipe_id, review_id):
    review = Review.objects.get(id=review_id)
    if req.user.is_authenticated:
        if review.reviewer.id != req.user.id:
            messages.error(req, "YOU CANNOT EDIT A REVIEW THAT IS NOT YOURS!")
            return redirect(f'/recipes/{recipe_id}')

        if req.method == 'GET':
            context = {
                'review': review
            }
            return render(req, 'reviews/edit_review.html', context)

        if req.method == 'POST':
            post_data = {
                'rating': req.POST['rating'],
                'comment': req.POST['comment']
            }
            errors = Review.objects.validate_review_data(post_data)
            if len(errors):
                for value in errors.values():
                    messages.error(req, value)
                return redirect(f'/recipes/{recipe_id}/reviews/{review.id}/edit/')
            for attr in post_data:
              if hasattr(review, attr):
                setattr(review, attr, post_data[attr])
            review.save()
            messages.success(req, "Your review has been updated successfully.")
            return redirect(f'/recipes/{recipe_id}')
    else:
        return redirect('/auth/login')

def delete_review(req,recipe_id, review_id):
  review = Review.objects.get(id=review_id)
  if req.user.is_authenticated:
    if review.user.id != req.user.id:
        messages.error(req, "YOU CAN NOT DELETE A REVIEW THAT IS NOT YOURS!")
        return redirect(f'/recipes/{recipe_id}')
    review.delete()
    return redirect(f'/recipes/{recipe_id}')
  else:
    return redirect('/auth/login')
