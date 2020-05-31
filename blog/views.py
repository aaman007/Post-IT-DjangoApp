from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse

def home(request):
    posts = Post.objects.all().order_by('-date_published')
    context = {
        'posts' : posts,
        'title' : 'Home'
    }
    return render(request, "blog/home.html", context)

def about(request):
    return render(request, "blog/about.html", { 'title' : 'About' })
