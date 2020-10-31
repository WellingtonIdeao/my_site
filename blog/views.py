from django.shortcuts import get_object_or_404
from .models import *
from django.views.generic import ListView
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            post = Post.objects.filter(title__icontains=query)
        else:
            post = Post.objects.all()
        return post


class PostView(ListView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])


class PostByCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):

        return Post.objects.filter(categories__name__iexact=self.kwargs['category'])
















