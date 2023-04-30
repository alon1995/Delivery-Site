from django.urls import path
from . import views

urlpatterns = [
    path('create_delivery/',views.create_delivery,name="create-delivery"),
    path('delivery_complete/<int:delivery_id>/',views.delivery_complete,name="delivery-complete"),
    path('show_cart/',views.show_cart,name="show-cart"),
    path('add_to_cart/<int:dish_id>/',views.add_to_cart,name="add-to-cart"),
    path('delete_item/<int:item_id>/',views.delete_from_cart,name="delete-from-cart"),
    path('reduce_item/<int:item_id>/',views.reduce_item_quantity,name="reduce-item-quantity"),
    path('orders_history',views.order_history,name="orders-history")
]