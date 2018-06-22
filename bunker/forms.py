from django import forms
from .models import Bunk

class BunkForm(forms.ModelForm):
    class Meta:
        model = Bunk
        fields = ['to_user']
