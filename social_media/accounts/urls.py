from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(),name='signup'),
    path('login/', auth_views.LoginView.as_view(form_class=forms.UserLoginForm),name='login'),
    #you can add attr here if you don't have them in views file
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
]