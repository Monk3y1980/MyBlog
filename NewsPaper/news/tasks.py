from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Category


@shared_task
def send_notify_mail():

    return None


@shared_task()
def send_newsletter():
    categories = Category.objects.all().exclude(title__gt=datetime.now() - timedelta(days=7))

    for category in categories:
        subscribers = User.objects.filter(subscription__title=id)
        subscribers_emails = []
        for user in subscribers:
            subscribers_emails.append(user.email)

            posts = Post.objects.filter(postcategory__category=id)
            content = render_to_string('news/newsletter.html',
                                       {'posts': posts,
                                        'category': category
                                        }
                                       )

        msg = EmailMultiAlternatives(
            subject=f'Новости за неделю',
            from_email='settings.DEFAULT_FROM_EMAIL',
            to=subscribers_emails,
            )
        msg.attach_alternative(content, "text/html")
        msg.send()
        print('Newsletter отправлен')