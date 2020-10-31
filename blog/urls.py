from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('post/', PostListView.as_view(), name='index'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/<slug:category>/', PostByCategory.as_view(), name='post_category')
]