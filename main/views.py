from django.shortcuts import render,redirect
from .models import Category,Dish
from django.contrib.admin.views.decorators import staff_member_required
from orders.views import get_cart_amount
from orders.models import Delivery,Cart,Item
from django.http import HttpResponse

# Create your views here.

def all_categorys(request):
    cart_amount = get_cart_amount(request)
    categorys = Category.objects.all()
    return render(request,'main/all_categories.html',{"categorys":categorys, "cart_amount":cart_amount})


def one_category(request,id):
    cart_amount = get_cart_amount(request)
    category = Category.objects.get(id=id)
    return render(request,'main/one_category.html',{"category":category, "cart_amount":cart_amount})


@staff_member_required
def manage_categorys(request):
    categorys = Category.objects.all()
    return render(request,'main/manage_categories.html',{"categorys":categorys})


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        new_category = Category (
            name = request.POST['name'],
            imageUrl = request.POST['imageUrl']
        )
        new_category.save()
        return redirect('manage-categories')
    return render(request,'main/add_category.html')


@staff_member_required
def delete_category(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage-categories')
    return render(request,'main/delete_category.html',{"category":category})


@staff_member_required
def edit_category(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.imageUrl = request.POST['imageUrl']
        category.save()
        return redirect('manage-categories')
    return render(request,'main/edit_category.html',{"category":category})


@staff_member_required
def manage_dishs(request,id):
    category = Category.objects.get(id=id)
    return render(request,'main/manage_dishs.html',{"category":category})


@staff_member_required
def add_dish(request):
    category = Category.objects.all()
    if request.method == 'POST':
        is_vegeterian = request.POST.get('vegeterian') == 'on'
        is_gluten_free = request.POST.get('gluten') == 'on'
        price = request.POST['price']
        if not price.isnumeric():
            return HttpResponse('<h1 style="color:red;">Error: Price must contain only numbers.</h1>')
        new_dish = Dish (
            name = request.POST['name'],
            imageUrl = request.POST['imageUrl'],
            price = price,
            description = request.POST['description'],
            is_vegeterian = is_vegeterian,
            is_gluten_free = is_gluten_free,
            category_id=request.POST['category_id']
        )
        new_dish.save()
        return redirect('manage-dishs',new_dish.category.id)
    return render(request,'main/add_dish.html',{"categorys":category})


@staff_member_required
def delete_dish(request,id):
    dish = Dish.objects.get(id=id)
    if request.method == 'POST':
        dish.delete()
        return redirect('manage-dishs',dish.category.id)
    return render(request,'main/delete_dish.html',{"dish":dish})


@staff_member_required
def edit_dish(request,id):
    dish = Dish.objects.get(id=id)
    if request.method == 'POST':
        is_vegeterian = request.POST.get('vegeterian') == 'on'
        is_gluten_free = request.POST.get('gluten') == 'on'
        dish.name = request.POST['name']
        dish.imageUrl = request.POST['imageUrl']
        dish.price = request.POST['price']
        dish.description = request.POST['description']
        dish.is_vegeterian = is_vegeterian
        dish.is_gluten_free = is_gluten_free
        dish.save()
        return redirect('one-category',dish.category.id)
    return render(request,'main/edit_dish.html',{"dish":dish})


@staff_member_required
def delivery_confirm(request):
    if request.method == 'POST':
        delivery_ids = request.POST.getlist('deliveries')
        for delivery_id in delivery_ids:
            if delivery_id:
                delivery = Delivery.objects.get(cart_id=delivery_id)
                delivery.is_delivered = True
                delivery.save()
                # get the cart objects for which delivery is complete
            carts = Cart.objects.filter(delivery__is_delivered=True).select_related('delivery')

            # delete the items for each cart where delivery is complete
            for cart in carts:
                items = Item.objects.filter(cart=cart)
                items.delete()
    deliveries = Delivery.objects.all()
    return render(request, 'main/delivery_confirm.html', {"deliveries": deliveries})


