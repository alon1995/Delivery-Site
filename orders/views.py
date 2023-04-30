from django.shortcuts import render,redirect
from .models import Delivery,Cart,Item
from main.views import Dish
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def get_cart_amount(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = Item.objects.filter(cart=cart)
        cart_amount = sum(item.amount for item in cart_items)
    else:
        cart_amount = 0
    return cart_amount

def get_or_create_cart(user):
    cart = Cart.objects.filter(user=user, delivery__isnull=True).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    return cart


@login_required(login_url='login')
def add_to_cart(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        item = Item.objects.filter(cart=cart, dish=dish).first()
        if item:
            item.amount += 1
            item.save()
        else:
            item = Item.objects.create(dish=dish, cart=cart, amount=1)
    else:
        cart = Cart.objects.create(user=request.user)
        item = Item.objects.create(dish=dish, cart=cart, amount=1)
    return redirect('one-category',dish.category.id)


@login_required(login_url='login')
def delete_from_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('show-cart')


@login_required(login_url='login')
def reduce_item_quantity(request, item_id):
    item = Item.objects.get(id=item_id)
    if item.amount > 1:
        item.amount -= 1
        item.save()
    else:
        item.delete()
    return redirect('show-cart')


@login_required(login_url='login')
def show_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = Item.objects.filter(cart=cart)
        cart_amount = get_cart_amount(request)
        total_price = sum(item.amount * item.dish.price for item in cart_items)
    else:
        cart_items = None
        cart_amount = 0
        total_price = 0
    latest_delivery = Delivery.objects.filter(cart__user=request.user).order_by('-cart_id').first()
    return render(request, 'orders/show_cart.html', {'cart_items': cart_items, 'cart_amount': cart_amount,'total_price': total_price,'latest_delivery':latest_delivery})


@login_required(login_url='login')
def create_delivery(request):
    user = request.user
    cart = get_or_create_cart(user=user)
    if request.method == 'POST':
        new_delivery = Delivery (
            adress = request.POST['adress'],
            comment = request.POST['comment'],
            cart = cart
        )
        new_delivery.save()
        return redirect("delivery-complete",new_delivery.cart.id)
    return render(request, 'orders/create_delivery.html')


@login_required(login_url='login')
def delivery_complete(request, delivery_id):
    delivery = Delivery.objects.get(pk=delivery_id)
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = Item.objects.filter(cart=cart)
    total_price = sum(item.amount * item.dish.price for item in cart_items)
    return render(request,'orders/delivery_complete.html',{"delivery":delivery,"total_price":total_price})


@login_required(login_url='login')
def order_history(request):
    deliveries = Delivery.objects.filter(cart__user=request.user)
    cart_amount = get_cart_amount(request)
    return render(request, 'orders/orders_history.html', {'deliveries': deliveries,"cart_amount":cart_amount})







