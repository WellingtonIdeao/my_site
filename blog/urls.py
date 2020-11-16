from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('noticias/', PostByCategory.as_view(), kwargs={'slug': 'noticias'}, name='news_list'),
    path('analises/', PostByCategory.as_view(), kwargs={'slug': 'analises'}, name='review_list'),
    path('especiais/', PostByCategory.as_view(), kwargs={'slug': 'especiais'}, name='special_list'),
    path('trophy-guides/', PostByCategory.as_view(), kwargs={'slug': 'trophy-guides'}, name='trophy_guides_list'),
    path('tag/<slug:slug>/', PostByTag.as_view(), name='post_by_tag_list'),
    path('<slug:slug>/', PostDetail.as_view(), name='post'),

]