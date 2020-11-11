from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('post/', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PageSelectView.as_view(), name='post'),
    path('post/tag/<slug:slug>/', PostByTag.as_view(), name='tag'),
]