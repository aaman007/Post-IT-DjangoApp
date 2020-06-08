from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from .forms import CommentForm
from .models import Comment
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


# def home(request):
#     posts = Post.objects.all().order_by('-date_published')
#     context = {
#         'posts' : posts,
#         'title' : 'Home'
#     }
#     return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_published']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    ordering = ['-date_published']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_published')


class PostDisplayView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDisplayView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_date')
        return context


class PostCommentView(CreateView):
    fields = ['content']
    model = Comment

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.filter(pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentView.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", { 'title' : 'About' })


def documentation(request):
    return render(request, "blog/api_documentation.html", { 'title' : 'API Documentation' })
