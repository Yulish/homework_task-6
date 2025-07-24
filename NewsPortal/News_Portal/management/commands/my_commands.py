from django.core.management.base import BaseCommand
from News_Portal.models import Author, Post, Category, PostCategory, Comment
1. user1 = User.objects.create_user('Tomas Shelby', password='tom')
user2 = User.objects.create_user('Alphy Solomons', password='alph')

2. author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

3. categories = ['Бизнес', 'Политика', 'Образование', 'Новости']
for category_name in categories:
Category.objects.create(category_name=category_name)

4. User.objects.all()
author = Author.objects.first()
author2 = Author.objects.all()[1]
business_cat = Category.objects.get(category_name='Бизнес')
politics_cat = Category.objects.get(category_name='Политика')

post1 = Post.objects.create(author=author, post_type=Post.ARTICLE, post_head='Курс доллара', post_text= 'Доллар сокрушительно падает относительно российского рубля')

post2 = Post.objects.create(author=author2, post_type=Post.ARTICLE, post_head='Россия одержала победу', post_text='Никто так и не смог дождаться того, чтобы Россия была побеждена на поле боя....')

post3 = Post.objects.create(author=author, post_type=Post.NEWS, post_head='Важная новость', post_text='Наконец-то закончилась СВО, продолжающаяся на протяжении трех с половиной лет...')

5. PostCategory.objects.create(post=post1, category=business_cat)
PostCategory.objects.create(post=post2, category=politics_cat)
PostCategory.objects.create(post=post3, category=politics_cat)
PostCategory.objects.create(post=post1, category=politics_cat)


6. Comment.objects.create(post=post1, user=user1, comment='Вот это поворот...')
Comment.objects.create(post=post2, user=user2, comment='Кто бы сомневался?!')
Comment.objects.create(post=post3, user=user1, comment='Слава Богу!')
Comment.objects.create(post=post3, user=user2, comment='Ура! Дождались!')
comments = Comment.objects.all()
for comment in comments:
print(comment)


7. post = Post.objects.get(id=1)
post.like()
post.dislike()
print('Рейтинг:', post.post_rate)
post = Post.objects.get(id=2)
post.like()
post.dislike()
post = Post.objects.get(id=3)
post.like()
post.dislike()

. comments = Comment.objects.get(id=1)
comments.like()
comments.dislike()
comments = Comment.objects.get(id=2)
comments.dislike()
print('Рейтинг:', comments.comment_rate)
Рейтинг: -1.0
comments.like()
comments = Comment.objects.get(id=3)
comments.like()
comments.dislike()
comments = Comment.objects.get(id=4)
comments.like()
comments.dislike()


8. rate = Author.objects.get(id=1)
rate.update_rating()
print(f'Рейтинг {rate.user.username}: {rate.author_rate}')

rate = Author.objects.get(id=2)
rate.update_rating()
print(f'Рейтинг {rate.user.username}: {rate.author_rate}')

9. best_author = Author.objects.order_by('-author_rate').first()
print(f'Лучший автор {best_author.user.username} с рейтингом {best_author.author_rate}')


10. best_article = Post.objects.filter(post_type='article').order_by('-post_rate').first()
print(f'Лучшая статья {best_article.post_head} автора {best_article.author} имеет рейтинг {best_article.post_rate}')

best_article = Post.objects.filter(post_type='article').order_by('-post_rate').first()
print(f'Лучшая статья "{best_article.post_head}" с рейтингом {best_article.post_rate} была добавлена автором {best_article.author} {best_article.post_origin.strftime("%d-%m-%Y %H:%M:%S")}, \nПревью: {best_article.preview()}')



11. article_com = Comment.objects.filter(post=best_article).order_by('comment_origin')

for data in article_com:
    print(f'Дата: {data.comment_origin.strftime("%d-%m-%Y %H:%M:%S")}, '
          f'Пользователь: {data.user.username}, '
          f'Рейтинг: {data.comment_rate}, '
          f'Текст: {data.comment}')
