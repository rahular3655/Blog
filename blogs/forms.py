from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field
from django import forms
from .models import Category

from froala.widget import FroalaEditor
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'content': FroalaEditor(),
        }

    user = AutoCompleteSelectField('users')  # To search in users dropdown in admin panel.
    category = AutoCompleteSelectField('category')
    tags = AutoCompleteSelectMultipleField('tags')
