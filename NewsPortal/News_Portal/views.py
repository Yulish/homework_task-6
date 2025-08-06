from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime, timezone


class NewsList(ListView):
    model = Post
    queryset = Post.objects.order_by('-post_origin')
    template_name = 'flatpages/newslist.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['next_news'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/idnews.html'
    context_object_name = 'news'



