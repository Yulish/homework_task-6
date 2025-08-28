from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth import get_user_model


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
        fields = ['post_head', 'post_text']
        labels = {
            'post_head': 'Заголовок',
            # 'author': 'Автор',
            'post_text': 'Введите текст',

        }

class Add_Change_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type','post_head', 'post_text', 'categories']
        labels = {
            'post_type': 'Выберите тип публикации: ',
            'post_head': 'Заголовок',
            'post_text': 'Введите текст',
            'categories': 'Категория',
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
            self.save_m2m()
        return post


User = get_user_model()

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    email = forms.EmailField(label='email', required=True)

    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput,
        required=True
    )
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
        required=False
    )
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['email'].initial = self.instance.email

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)

        # Проверка текущего пароля
        if self.cleaned_data.get('current_password'):
            if not user.check_password(self.cleaned_data['current_password']):
                raise forms.ValidationError("Текущий пароль неверен.")
            # Проверка нового пароля
            new_password = self.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)

        # Сохранение остальных полей
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
