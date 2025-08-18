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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse

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

class NewsUpdate(LoginRequiredMixin, UpdateView):
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

class ArticleUpdate(LoginRequiredMixin, UpdateView):
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


class LoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url   # куда пользователь хотел перейти
        else:
            return reverse('news/')  # по умолчанию, если next не указан

class GoogleCallbackView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri='https://127.0.0.1:8000/accounts/google/login/callback/'
        )
        flow.fetch_token(authorization_response=request.build_absolute_url())
        credentials = flow.credentials
        idinfo = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), '63012377443-oo6i317jejj7855feaqfod84fp82m2co.apps.googleusercontent.com')
        email = idinfo['email']
        name = idinfo['name']
        user, created = User.objects.get_or_create(email=email, defaults={'username': name})
        login(request, user)
        return redirect('/news')

def google_login(request):
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri='https://127.0.0.1:8000/accounts/google/login/callback/'
        )
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)

class YandexCallbackView(View):
    def get(self, request):
        # Получение кода из запроса
        code = request.GET.get('code')
        if not code:
            return HttpResponse("Ошибка: отсутствует код авторизации.", status=400)

        # Запрос на получение токена
        token_url = 'https://oauth.yandex.ru/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': '69da15e29df8499bbefdabb5a021a621',  # Ваш client_id
            'client_secret': 'ecc3e9c7ebd24842a83e809cf7c66495',  # Ваш client_secret
        }

        # Отправка POST-запроса на получение токена
        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            return HttpResponse("Ошибка при получении токена: {}".format(response.json().get('error')), status=400)

        token_info = response.json()
        access_token = token_info.get('access_token')

        # Запрос на получение информации о пользователе
        user_info_url = 'https://api.yandex.ru/v1/userinfo'
        headers = {
            'Authorization': f'OAuth {access_token}',
        }

        user_info_response = requests.get(user_info_url, headers=headers)
        if user_info_response.status_code != 200:
            return HttpResponse(
                "Ошибка при получении информации о пользователе: {}".format(user_info_response.json().get('error')),
                status=400)

        user_info = user_info_response.json()
        email = user_info.get('email')
        name = user_info.get('name')

        # Создание или получение пользователя в базе данных
        user, created = User.objects.get_or_create(email=email, defaults={'username': name})
        login(request, user)

        return redirect('/')


def get_yandex_auth_url():
    client_id = '69da15e29df8499bbefdabb5a021a621'  # Ваш client_id
    redirect_uri = 'https://127.0.0.1:8000/accounts/yandex/login/callback/'  # Ваш redirect_uri
    auth_url = (
        f'https://oauth.yandex.ru/authorize?response_type=code'
        f'&client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
    )
    return auth_url

def login_view(request):
    return render(request, 'sign/login.html')

















