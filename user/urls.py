from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_user,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logout_user,name="logout"),
    path('update-user/<int:user_id>/', views.update_user, name='update-user'),
]