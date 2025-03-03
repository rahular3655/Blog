from django import forms

from froala.widget import FroalaEditor
from .models import Regulations


class RegulationsForm(forms.ModelForm):
    class Meta:
        model = Regulations
        fields = '__all__'
        widgets = {
            'value': FroalaEditor(),
        }
