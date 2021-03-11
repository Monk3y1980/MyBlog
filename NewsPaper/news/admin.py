from django.contrib import admin
# импортируем модель амдинки (вспоминаем модуль про переопределение
from modeltranslation.admin import TranslationAdmin
from .models import Author, Category, Post, Comment, PostAdmin

admin.site.register(Post)


class PostAdmin(TranslationAdmin):
    model = Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating')
    list_filter = ['author']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    filter_horizontal = ['subscribers']
    search_fields = ('title', 'postcategory__category__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'comment_post', 'comment_text', 'comment_created', 'comment_rating', 'comment_likes', 'comment_dislikes')

