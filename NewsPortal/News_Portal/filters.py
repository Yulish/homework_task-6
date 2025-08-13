from django_filters import FilterSet
from .models import Post
import django_filters
from django import forms



class NewsFilter(FilterSet):
    author_username = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Фамилия автора')
    post_head = django_filters.CharFilter(lookup_expr='icontains', label='Название статьи')
    date_from = django_filters.DateFilter(
        field_name='post_origin',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Показать статьи после даты'
    )


