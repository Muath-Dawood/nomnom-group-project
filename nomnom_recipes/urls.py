from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recipes_index'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('contact/', views.contact, name='contact'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('recipes/', views.all_recipes, name='recipes_list_recipes'),
    path('recipes/add/', views.add_recipe, name='recipes_add_recipe'),
    path('recipes/<int:id>/', views.show_recipe, name='recipes_show_recipe'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='recipes_edit_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='recipes_delete_recipe'),
    path('recipes/<int:id>/reviews/add/', views.add_review, name='recipes_add_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/edit/', views.edit_review, name='recipes_edit_review'),
    path('recipes/<int:recipe_id>/reviwes/<int:review_id>/delete/', views.delete_review, name='recipes_delete_review'),
    path('search', views.search, name='search'),
]
