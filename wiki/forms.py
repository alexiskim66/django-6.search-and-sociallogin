from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'writer', 'body', 'image']


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')