from django.urls import path
from .views import NewsPaperLoginView, NewsPaperLogOutView, NewsPaperRegisterView, upgrade_me

urlpatterns = [
    path('login/', NewsPaperLoginView.as_view(), name='login'),
    path('register/', NewsPaperRegisterView.as_view(), name='register'),
    path('logout/', NewsPaperLogOutView.as_view(), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade')
    ]