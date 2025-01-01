from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='nomnom_recipes_index'),
    path('recipes/', views.all_recipes, name='all_recipes'),
    path('recipes/my_recipes/', views.my_recipes, name='my_recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:id>/', views.show_recipe, name='show_recipe'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:id>/reviews/add/', views.add_review, name='add_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/delete/', views.delete_recipe, name='delete_recipe'),
]
