from django.urls import path
from . import views

urlpatterns = [
    path('',views.all_categorys,name="all-categories"),
    path('category/<int:id>',views.one_category,name="one-category"),
    path('manage_categories',views.manage_categorys,name="manage-categories"),
    path('add_category/',views.add_category,name="add-category"),
    path('category_d/<int:id>',views.delete_category,name="delete-category"),
    path('category_e/<int:id>',views.edit_category,name="edit-category"),
    path('manage_dishs/<int:id>',views.manage_dishs,name="manage-dishs"),
    path('add_dish/',views.add_dish,name="add-dish"),
    path('dish_d/<int:id>',views.delete_dish,name="delete-dish"),
    path('edit_d/<int:id>',views.edit_dish,name="edit-dish"),
    path('delivery_confirm',views.delivery_confirm,name="delivery-confirm"),
]