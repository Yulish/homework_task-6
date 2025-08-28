from datetime import datetime, timezone
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in, user_signed_up
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import PostCategory, Appointment, Post, Author
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail, mail_admins, mail_managers
from django.dispatch import receiver
# from .views import AddPost
from django.core.exceptions import ValidationError

@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    pass

@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    pass


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)



def send_notifications(preview, pk, title, post, subscribers):
    html_content = render_to_string('post_created_email.html',
                                    {'text': preview, 'link': f'{settings.SITE_URL}/news/{pk}'})
    if post and hasattr(post, 'post_type'):
        if Post.NEWS:
            html_content = render_to_string('post_created_email.html',
                                        {'text': preview, 'link': f'{settings.SITE_URL}/news/{pk}'})
        else:
            html_content = render_to_string('article_created_email.html',
                                        {'text': preview, 'link': f'{settings.SITE_URL}/articles/{pk}'})

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver (m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.post_head, instance.post_type, subscribers_emails)

@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject=f'{instance.client_name}{instance.date.strftime("%d %m %Y")}',
        message=instance.message
    else:
        subject=f'Something changed for {instance.client_name}{instance.date.strftime("%d %m %Y")}',
        message=instance.message
    mail_managers(
        subject=subject,
        message=instance.message
    )




