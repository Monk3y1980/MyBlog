from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin
from django.core.cache import cache
from django.utils.translation import pgettext_lazy  # импортируем «ленивый» геттекст с подсказкой
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, unique=True, verbose_name='Автор')
    rating = models.IntegerField('Рейтинг', auto_created=True, default=0)

    def __str__(self):
        return '%s' % self.author

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self, rating):
        self.rating = rating
        value_post = Author.objects.filter(Post.post_rating)  # Каждой статьи автора
        value_post = value_post * 3
        value_auth = Author.objects.filter(Comment.comment_rating)  # всех комментариев автора
        value_comment = Author.objects.filter(Post.post_rating, Comment.comment_rating)  # всех комментариев к статьям автор
        value = value_post + value_auth + value_comment

        self.rating = value
        return value


class Category(models.Model):
    title = models.CharField('Категория', unique=True, max_length=120, help_text=_('category name'))
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscription', verbose_name='Подписчики')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(models.Model):
    news = 'Новость'
    article = 'Статья'
    Posts = [(news, 'Новость'), (article, 'Статья'), ('select', 'Выбрать')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    post_theme = models.CharField(max_length=30, choices=Posts, default='select', verbose_name='Тема')
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категории')
    post_title = models.CharField('Заголовок', max_length=50)
    post_text = models.TextField('Текст')
    post_rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    post_likes = models.IntegerField(default=0, verbose_name='Понравилось')
    post_dislikes = models.IntegerField(default=0, verbose_name='Не понравилось')

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с постами
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.post_author}: {self.post_title}: {self.post_text}| {self.created}'

    def preview(self):
        if len(self.post_text) > 124:
            text_string = self.post_text[:124] + '...'
        else:
            text_string = self.post_text
        return text_string

    def like(self):
        self.post_likes += 1
        self.save()

    def dislike(self):
        self.post_dislikes += 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')

    def __str__(self):
        return '%s' % self.category


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Комментарии пользователя')
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментарии к публикации')
    comment_text = models.CharField('Текст комментария', max_length=80)
    comment_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comment_rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    comment_likes = models.IntegerField(default=0, verbose_name='Понравилось')
    comment_dislikes = models.IntegerField(default=0, verbose_name='Не понравилось')

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.comment_likes += 1
        self.save()

    def dislike(self):
        self.comment_dislikes += 1
        self.save()


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]

