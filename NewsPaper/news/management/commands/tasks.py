from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from news.models import Post, Category


def send_newsletter():
    if datetime.isoweekday(datetime.now()) == 1:
        week = localtime() - timedelta(days=7)
        categories = Category.objects.all()

        for category in categories:
            subscribers = User.objects.filter(subscription__title=category)
            subscribers_emails = []
            for user in subscribers:
                subscribers_emails.append(user.email)

                posts = Post.objects.filter(postcategory__category=category, date_create__gt=week)
                content = render_to_string('news/newsletter.html',
                                           {'posts': posts,
                                            'category': category,
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



