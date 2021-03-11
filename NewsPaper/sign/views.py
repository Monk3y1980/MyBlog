from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .forms import RegisterUser, AuthUserForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from news.models import Author
# from django.contrib.auth.mixins import LoginRequiredMixin


class NewsPaperLoginView(LoginView):
    template_name = 'sign/login.html'
    form_class = AuthUserForm
    next_page = '/protect/index/'


class NewsPaperRegisterView(CreateView):
    template_name = 'sign/register.html'
    form_class = RegisterUser
    success_url = '/sign/login'


class NewsPaperLogOutView(LogoutView):
    template_name = 'sign/logout'
    next_page = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author = User.objects.get(username=user)
        Author.objects.create(author=author)
        authors_group.user_set.add(user)
    return redirect('/')