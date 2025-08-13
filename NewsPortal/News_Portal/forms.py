from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class ViewsForm(forms.ModelForm):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Показать новости после даты'
    )
    class Meta:
        model = Post
        fields = ['post_head', 'author']




class CreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_head', 'author', 'post_text']
        labels = {
            'post_head': 'Заголовок',
            'author': 'Автор',
            'post_text': 'Введите текст',
        }





