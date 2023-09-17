from django import forms
from .models import Eminem

class ImageForm(forms.ModelForm):
    class Meta:
        model = Eminem
        fields = ['image']