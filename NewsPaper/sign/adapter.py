from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


# функция переопределения редиректов allauth
class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = '/news'
        return path.format(username=request.user.username)

    def get_logout_redirect_url(self, request):
        path = '/news'
        return path

    def get_signup_redirect_url(self, request):
        path = '/news'
        return path


# функция переопределения формы регистрации allauth через соц сети
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # с помощью super выполняем свой библиотеке, и дальнее добавим свой
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form=None)
        # Вытаскиваем из бд группу common и прикрепляем к нему нового пользователя
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        # Создаем профиль для нового пользователя
        return user