from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from django.contrib.auth.models import User


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.post_category.through)
def notify_post(instance, **kwargs):
# Наблюдаем категорию, которая была изменена
    changed_category = Category.objects.filter(postcategory__post=instance)
    if changed_category.count() == 1:
        # Достаем через гет измененную категорию
        category = Category.objects.get(postcategory__post=instance)
        # Собираем всех пользователей, подписанных на данную категорию
        subscribers = User.objects.filter(subscription__title=category)
        # Создаем списаок емейл адресов из пользователей
        email_subscribers = []
        for email in subscribers:
            email_subscribers.append(email.email)

        # Создаем html для передачи рассылки
        category = f'{instance.post_category}'
        text = f'{instance.post_text}'
        theme = f'{instance.post_title}'
        # Достаем ид добавленной новости, для формирования ссылки
        url = f'{Post.objects.get(postcategory__post=instance).id}'

        msg = EmailMultiAlternatives(
            subject='Появились обновления в категории на которую вы подписаны',
            from_email='mail',
            to=email_subscribers,
        )
        content = render_to_string('news/create_email.html', {
            'category': category,
            'theme': theme,
            'text': text,
            'url': url,
                }
        )
        msg.attach_alternative(content, "text/html")  # добавляем html
        msg.send()  # отсылаем
