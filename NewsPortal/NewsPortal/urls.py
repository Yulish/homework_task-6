from django.contrib import admin
from django.urls import path, include
from News_Portal.views import (NewsList, NewsDetail, NewsSearch,
                               ArticleList, ArticleDetail, ArticleCreate, NewsCreate, NewsUpdate,
                               NewsDelete, ArticleUpdate, ArticleSearch)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', NewsList.as_view(), name='news_list'),# это просто свое название
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name = 'news_update'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name = 'article_update'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='article_delete'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),
]




