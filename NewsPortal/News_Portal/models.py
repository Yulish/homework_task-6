from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.db.models import Sum
from decimal import Decimal, InvalidOperation
from django.urls import reverse



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    def __str__(self):
        return self.user.username

    def update_rating(self):
        sum_article_rate = (self.post_set.aggregate(total_rate=Sum('post_rate'))['total_rate'] or 0) * 3

        sum_author_comments_rate = self.user.comment_set.aggregate(total_rate=Sum('comment_rate'))['total_rate'] or 0
        sum_post_comment_rate = Comment.objects.filter(post__author=self).aggregate(total_rate=Sum('comment_rate'))[
                                'total_rate'] or 0
        self.author_rate = (sum_article_rate + sum_author_comments_rate + sum_post_comment_rate)
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ARTICLE = 'article'
    NEWS = 'news'
    POST_CHOICES = [(ARTICLE, 'статья'), (NEWS, 'новость')]
    post_type = models.CharField(max_length=10, choices=POST_CHOICES, default=NEWS)
    categories = models.ManyToManyField(Category, through = 'PostCategory')
    post_origin = models.DateTimeField(auto_now_add=True)
    post_head = models.CharField(max_length=255, default=0)
    post_text = models.TextField(max_length=100000, default=0)
    post_rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def like(self):
        self.post_rate = self.post_rate + 1
        self.save()

    def dislike(self):
        self.post_rate = self.post_rate - 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'

    def __str__(self):
        return self.post_head

    def get_absolute_url(self):
        return reverse('news_search', args=[str(self.id)])

    def get_detail_url(self):
        if self.post_type == self.NEWS:
            return reverse('news_detail', args=[str(self.id)])
        elif self.post_type == self.ARTICLE:
            return reverse('article_detail', args=[str(self.id)])
        # Если тип поста не соответствует ни NEWS, ни ARTICLE, можно вернуть None или выбросить исключение
        return None




class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.post.post_head} - {self.category.category_name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_origin = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000)
    comment_rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f"{self.user.username}: {self.comment[:50]}"

    def like(self):
        self.comment_rate = self.comment_rate + 1
        self.save()

    def dislike(self):
        self.comment_rate = self.comment_rate - 1
        self.save()




