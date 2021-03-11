from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .tasks import send_notify_mail
from django.core.cache import cache
from django.utils.translation import gettext as _


class PostList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'posts'
    paginate_by = 3
    ordering = ['-created']


class PostListDetails(DetailView):
    template_name = 'news/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует
        # также. Он забирает значение по ключу, если его нет, то забирает None.

    # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.view_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_author = Author.objects.get(author=self.request.user)
        self.object.save()
        send_notify_mail.apply_async()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_update.html'
    permission_required = ('news.change_post', 'news.view_post')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post', 'news.view_post')


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя
        # метод get_context_data у наследуемого класса

        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCategoryList(LoginRequiredMixin, ListView):
    template_name = 'news/post_category.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()


class PostCategoryDetails(LoginRequiredMixin, DetailView):
    template_name = 'news/category.html'
    context_object_name = 'category'
    queryset = Category.objects.all()


class AddSubscribers(UpdateView):
    template_name = 'news/category.html'
    model = Category
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(User.objects.get(username=str(user)))
        return redirect('/')


#class RemoveSubscribers(DetailView):
#    template_name = 'news/category.html'
#    model = Category
#    success_url = 'news/category.html'









