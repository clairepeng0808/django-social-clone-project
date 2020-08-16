from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from . import forms
from django.views.generic import CreateView,FormView
from django.contrib.auth.views import LoginView

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login') 
    # once they sign up successfully, reverse them to the login page