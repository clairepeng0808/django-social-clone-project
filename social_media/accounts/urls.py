from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(),name='signup'),
    path('login/', auth_views.LoginView.as_view(form_class=forms.UserLoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
]