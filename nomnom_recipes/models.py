from django.db import models
from django.contrib.auth import get_user_model
import uuid
from PIL import Image
import os

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
    if not post_data['image']:
      errors['no_instructions'] = "You must include an image!"
    return errors

class ReviewManager(models.Manager):
  def validate_review_data(self, post_data):
    errors = {}
    if 'rating' not in post_data or not (1 <= int(post_data['rating']) <= 5):
      errors['invalid_rating'] = "Rating must be an integer between 1 and 5."
    if 'comment' in post_data and len(post_data['comment']) > 500:
      errors['long_comment'] = "Comment must be 500 characters or fewer."
    return errors


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RecipeManager()

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
          sum = 0
          for review in reviews :
              sum += review.rating
          return sum/len(reviews)
        return 0

    def save(self, *args, **kwargs):
        # is instance new
        is_new_instance = self.pk is None

        # Retrieve the previous value of profile_pic if the instance exists
        if not is_new_instance:
            old_instance = Recipe.objects.filter(pk=self.pk).first()
            old_image = old_instance.image if old_instance else None
        else:
            old_image = None

        # Call the original save method first to ensure a pk is generated
        super().save(*args, **kwargs)

        # if instance is new or if profile_pic is updated
        if is_new_instance or self.image != old_image:
            if self.image:
                img_path = self.image.path
                img = Image.open(img_path)
                target_width = 320

                if img.width > target_width:
                    ratio = target_width / float(img.width)
                    target_height = int(float(img.height) * ratio)
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    img.save(img_path)

                # Rename the file to include a unique identifier
                unique_name = f"{uuid.uuid4()}{os.path.splitext(img_path)[1]}"
                new_path = os.path.join(os.path.dirname(img_path), unique_name)
                os.rename(img_path, new_path)
                self.image.name = os.path.relpath(new_path, os.path.dirname(new_path)[:-8])
                super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    def __str__(self):
        return f"{self.reviewer.username} - {self.recipe.title} ({self.rating}/5)"

