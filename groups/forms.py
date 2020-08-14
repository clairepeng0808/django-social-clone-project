from django import forms
from . import models

class GroupForm(forms.ModelForm):

    class Meta():
        model = models.Group
        fields = ('name','description')