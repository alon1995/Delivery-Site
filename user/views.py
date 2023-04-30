from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        if not first_name.isalpha():
            return HttpResponse('<h1 style="color:red;">Error: First and last name must contain only letters.</h1>')
        new_user = User(
            first_name = first_name,
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = make_password(request.POST['password'])
        )
        new_user.save()

        return redirect('login')
    return render(request,'user/signup.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('all-categories')
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('all-categories')
    return render(request,'user/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        user.password = make_password(request.POST['password'])
        user.save()
        return redirect('login')
    return render(request, 'user/update_user.html', {'user':user})


