from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author
from allauth.account.signals import user_logged_in, user_signed_up
from django.shortcuts import redirect
from django.urls import reverse

# @receiver(user_logged_in)
# def on_user_logged_in(request, user, **kwargs):
#     pass
#
# @receiver(user_signed_up)
# def on_user_signed_up(request, user, **kwargs):
#     pass


@receiver(post_save, sender=User )
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
