from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm)
from django import forms
from . import models


class UserCreateForm(UserCreationForm):
    # don't use the same name as the built-in name
    
    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()
 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'

        self.fields['email'].label = 'Email Address'
        self.fields['email'].widget.attrs.update({'placeholder': 'starsocial@example.com'})
    

        self.fields['password1'].label = 'Set Password'

        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''

class UserLoginForm(AuthenticationForm):
    
    class Meta:
        model = get_user_model()
        fields = ('username','password')
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Your Username'
        
 
