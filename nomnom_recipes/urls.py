from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recipes_index'),
    path('recipes/', views.all_recipes, name='recipes_list_recipes'),
    path('recipes/my_recipes/', views.my_recipes, name='recipes_my_recipes'),
    path('recipes/add/', views.add_recipe, name='recipes_add_recipe'),
    path('recipes/<int:id>/', views.show_recipe, name='recipes_show_recipe'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='recipes_edit_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='recipes_delete_recipe'),
    path('recipes/<int:id>/reviews/add/', views.add_review, name='recipes_add_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/edit/', views.edit_review, name='recipes_edit_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/delete/', views.delete_recipe, name='recipes_delete_review'),
]
