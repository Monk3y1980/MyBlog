from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['post_theme', 'post_category', 'post_title', 'post_text']

        widgets = {
            'post_title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи или новости'
            }),
            'post_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),

            'post_theme': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать...'
            }),
            'post_category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
        }
