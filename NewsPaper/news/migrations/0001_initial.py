# Generated by Django 3.1.7 on 2021-03-11 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(auto_created=True, default=0, verbose_name='Рейтинг')),
                ('author', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='category name', max_length=120, unique=True, verbose_name='Категория')),
                ('title_de', models.CharField(help_text='category name', max_length=120, null=True, unique=True, verbose_name='Категория')),
                ('title_ru', models.CharField(help_text='category name', max_length=120, null=True, unique=True, verbose_name='Категория')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_theme', models.CharField(choices=[('Новость', 'Новость'), ('Статья', 'Статья'), ('select', 'Выбрать')], default='select', max_length=30, verbose_name='Тема')),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('post_title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('post_text', models.TextField(verbose_name='Текст')),
                ('post_text_de', models.TextField(null=True, verbose_name='Текст')),
                ('post_text_ru', models.TextField(null=True, verbose_name='Текст')),
                ('post_rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('post_likes', models.IntegerField(default=0, verbose_name='Понравилось')),
                ('post_dislikes', models.IntegerField(default=0, verbose_name='Не понравилось')),
                ('post_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категории')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.Category', verbose_name='Категории'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=80, verbose_name='Текст комментария')),
                ('comment_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('comment_rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('comment_likes', models.IntegerField(default=0, verbose_name='Понравилось')),
                ('comment_dislikes', models.IntegerField(default=0, verbose_name='Не понравилось')),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Комментарии к публикации')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Комментарии пользователя')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
