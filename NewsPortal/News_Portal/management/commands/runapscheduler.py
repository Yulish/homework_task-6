import datetime
import logging
from sched import scheduler

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

# from News_Portal.management.commands.my_commands import category_name
from News_Portal.models import Post, Category
from News_Portal.views import subscribe

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_origin__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новые публикации в ваших подписках за неделю:',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="thu", hour="21", minute="01"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        scheduler.start()

        import time
        while True:
            time.sleep(1)
