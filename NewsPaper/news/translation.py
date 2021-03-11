from .models import *
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_text', )  # указываем, какие именно поля надо переводить в виде кортежа


@register(Category)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', )  # указываем, какие именно поля надо переводить в виде кортежа