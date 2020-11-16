from .models import *
from django.views.generic import ListView, DetailView
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


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostByTag(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])


class PostByCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(categories__slug=self.kwargs['slug'])


'''class PageSelectView(View):

    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(slug=self.kwargs['slug'])
            view = PostByCategory.as_view()
        except Category.DoesNotExist:
            view = PostDetail.as_view()
        return view(request, *args, **kwargs)

class PostView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = Comment(post=self.object, author=self.object.author)
        form = CommentModelForm(instance=comment)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form = CommentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:post', args=(post.id, )))
'''



















