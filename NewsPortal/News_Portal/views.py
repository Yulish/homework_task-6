from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datetime import datetime, timezone
from .filters import NewsFilter
from django.urls import reverse_lazy
from .models import Post
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ViewsForm, CreateForm
from django.urls import reverse

class NewsList(ListView):
    model = Post
    queryset = Post.objects.order_by('-post_origin')
    template_name = 'flatpages/newslist.html'
    context_object_name = 'news'
    paginate_by = 2
    items = list(range(1, len(Post.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['next_news'] = None
        return context

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-post_origin')


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/idnews.html'
    context_object_name = 'news' # берется из модели POST NEWS = 'news'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')

class NewsSearch(ListView):
    model = Post
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type=Post.NEWS).order_by('-post_origin')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    form_class = CreateForm
    model = Post
    template_name = 'flatpages/news_create.html'
    success_url = reverse_lazy('news_list') # берется из urls

    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)




class NewsUpdate(UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'flatpages/news_edit.html'
    success_url = reverse_lazy('news_update')

    def get_success_url(self):
        return reverse('news_detail', kwargs={'pk': self.object.pk})

class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('news_list')



class ArticleList(ListView):
    model = Post
    queryset = Post.objects.order_by('-post_origin')
    template_name = 'flatpages/article.html'
    context_object_name = 'article' # берется из модели POST ARTICLE = 'article'
    paginate_by = 2
    items = list(range(1, len(Post.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['next_news'] = None
        return context

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-post_origin')

class ArticleDetail(DetailView):
    model = Post
    template_name = 'flatpages/idarticle.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')

class ArticleSearch(ListView):
    model = Post
    template_name = 'flatpages/article_search.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type=Post.ARTICLE).order_by('-post_origin')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context




class ArticleCreate(CreateView):
    form_class = CreateForm
    model = Post
    template_name = 'flatpages/article_create.html'
    success_url = reverse_lazy('article_list') # берется из urls, показывает страницу перенаправления

    def form_valid(self, form):
        form.instance.post_type = 'article'  # или 'news' для NewsCreate
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'flatpages/article_edit.html'
    success_url = reverse_lazy('article_update')

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.pk})

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/article_delete.html'
    success_url = reverse_lazy('article_list')










