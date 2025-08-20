from datetime import datetime, timezone
from .filters import NewsFilter
from .models import Post, Author
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProfileForm, Add_Change_Form
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect

User = get_user_model()


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



class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/article_delete.html'
    success_url = reverse_lazy('article_list')

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<News_Portal>.<add>_<Post>',
                           '<News_Portal>.<change>_<Post>')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('News_Portal.add_post',)
    model = Post
    form_class = Add_Change_Form

    def get_template_names(self):
        return ['flatpages/article_create.html']

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        form.save()

        if form.instance.post_type == 'news':
            self.success_url = reverse_lazy('news_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/news_create.html'
        else:
            self.success_url = reverse_lazy('article_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/article_create.html'
        return super().form_valid(form)

class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('News_Portal.change_post',)
    model = Post
    form_class = Add_Change_Form

    def get_template_names(self):
        return ['flatpages/article_edit.html']

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        form.save()
        if form.instance.post_type == 'news':
            self.success_url = reverse_lazy('news_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/news_edit.html'
        else:
            self.success_url = reverse_lazy('article_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/article_edit.html'

        return super().form_valid(form)


# @method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
        print("Метод GET вызван")  # Добавьте это сообщение
        author = get_object_or_404(User, id=pk)
        is_not_authors = not request.user.groups.filter(name='authors').exists()
        context = {
            'author': author,
            'user': request.user,
            'is_not_authors': is_not_authors,
        }
        return render(request, 'allauth/layouts/base.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        print(f"Пользователь: {request.user.username}, is_not_authors: {is_not_authors}")
        return context

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile_edit.html'

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[pk]))
        else:
            return render(request, 'profile_update.html', {'form': form, 'user': user})


class IndexView(TemplateView):
    template_name = 'main_page.html'





@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

