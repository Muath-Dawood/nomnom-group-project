from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class RecipeManager(models.Manager):
  def validate_recipe_data(self, post_data):
    errors = {}
    if not post_data['title']:
      errors['no_title'] = "You must fill the Title field!"
    if not post_data['description']:
      errors['no_description'] = "You must fill the Description field!"
    if not post_data['ingredients']:
      errors['no_ingredients'] = "You must fill the Ingredients field!"
    if not post_data['instructions']:
      errors['no_instructions'] = "You must fill the instructions field!"
    return errors


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='images/recipes/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def average_rating(self):
        reviews = self.reviews.objects.all()
        sum = 0
        for review in reviews : 
            sum += review.rating 
        return sum/len(reviews)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.recipe.title} ({self.rating}/5)"

