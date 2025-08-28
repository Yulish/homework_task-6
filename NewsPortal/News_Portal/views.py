from datetime import datetime, timezone
from .filters import NewsFilter
from .forms import Add_Change_Form, ProfileForm
from .models import Post, Author, Category, Appointment
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import ProfileForm, Add_Change_Form
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives, send_mail, mail_admins, mail_managers
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class NewsList(ListView):  # post
    model = Post
    template_name = 'flatpages/newslist.html'
    context_object_name = 'posts'
    paginate_by = 10
    items = list(range(1, len(Post.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['categories'] = Category.objects.all()
        context['next_news'] = None
        category_id = self.request.GET.get('category_id')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type=Post.NEWS).order_by('-post_origin')
        self.filterset = NewsFilter(self.request.GET, queryset)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset.order_by('-post_origin')


class NewsCategory(NewsList):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category, post_type=Post.NEWS).order_by('-post_origin')
        return queryset

    def get_context_data(self, **kwargs):  # кнопка подписаться
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/idnews.html'
    context_object_name = 'news'

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
    context_object_name = 'article'  # берется из модели POST ARTICLE = 'article'
    paginate_by = 10
    items = list(range(1, len(Post.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['categories'] = Category.objects.all()
        context['next_news'] = None
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type=Post.ARTICLE).order_by('-post_origin')
        self.filterset = NewsFilter(self.request.GET, queryset)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset.order_by('-post_origin')


class ArticleCategory(ArticleList):
    model = Post
    template_name = 'flatpages/art_category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category, post_type=Post.ARTICLE).order_by('-post_origin')
        return queryset

    def get_context_data(self, **kwargs):  # кнопка подписаться
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


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

        post_date = datetime.now(timezone.utc).date()
        post_amount = Post.objects.filter(
            author=author,
            post_origin__date=post_date
        ).count()

        if post_amount >= 3:
            messages.error(self.request, "❌ Превышен лимит публикаций (3 поста в день)")
            return self.render_to_response(self.get_context_data(form=form))
        post = form.save(commit=False)
        post.save()
        form.save_m2m()

        if form.instance.post_type == 'news':
            # self.success_url = reverse('news_detail', kwargs={'pk': post.pk})
            self.success_url = reverse_lazy('news_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/news_create.html'
        else:

            # self.success_url = reverse('article_detail', kwargs={'pk': post.pk})
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
            self.success_url = reverse('news_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/news_edit.html'
        else:
            self.success_url = reverse('article_detail', kwargs={'pk': form.instance.pk})
            self.template_name = 'flatpages/article_edit.html'

        return super().form_valid(form)


# @method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
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

    def get_form_class(self):
        return ProfileForm


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


@login_required
def subscribe(request, pk):
    user = request.user  # получаем текущего пользователя
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)  #добавляем в число подписчиков

    message = 'Вы успешно подписались на категорию: '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user  # получаем текущего пользователя
    category = Category.objects.get(id=pk)
    if user in category.subscribers.all():
        category.subscribers.remove(user)

    message = 'Вы отписались от рассылки постов в категории: '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment_make.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        mail_managers(
            subject=f'{instance.client_name}{instance.date.strftime("%d %m %Y")}',
            message=instance.message
        )
        return redirect('appointment')
