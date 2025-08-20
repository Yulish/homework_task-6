from django.contrib import admin
from django.urls import path, include
from News_Portal.views import (NewsList, NewsDetail, NewsSearch,
                               ArticleList, ArticleDetail, IndexView,
                               NewsDelete, ArticleSearch, upgrade_me,
                               ProfileUpdate, ProfileView, AddPost, ChangePost)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', NewsList.as_view(), name='news_list'),# это просто свое название
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/edit/', ChangePost.as_view(), name = 'news_update'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', AddPost.as_view(), name='news_create'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', AddPost.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ChangePost.as_view(), name = 'article_update'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='article_delete'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),
    path('post/add', AddPost.as_view(), name='add_post'),
    path('accounts/', include('allauth.urls')),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    # path('redirect-profile/', redirect_to_profile, name='redirect_to_profile'),
    path('users/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('users/<int:pk>/profile_update/', ProfileUpdate.as_view(), name='profile_update'),

]




