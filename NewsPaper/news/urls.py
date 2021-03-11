from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>/', PostListDetails.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('categories/', PostCategoryList.as_view(), name='post_category'),
    path('<int:pk>/', PostCategoryDetails.as_view(), name='subscribe'),
    path('categories/<int:pk>/add', AddSubscribers.as_view(), name='subscribe'),
#    path('categories/<int:pk>/remove', RemoveSubscribers.as_view(), name='subscribe'),
]