from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='nomnom_recipes_index'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:id>/', views.show_recipe, name='show_recipe'),
    path('recipe/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:id>/add_review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
]
