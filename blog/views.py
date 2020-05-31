from django.shortcuts import render
# from django.http import HttpResponse

posts = [
    {
        'author' : 'aaman007',
        'title' : 'Abracadabra',
        'content' : 'This is a magical post',
        'date_posted' : '31st May, 2020'
    },
    {
        'author' : 'Decayed',
        'title' : 'Abracadabra2',
        'content' : 'This is also a magical post',
        'date_posted' : '1st June, 2020'
    }
]

def home(request):
    context = {
        'posts' : posts,
        'title' : 'Home'
    }
    return render(request, "blog/home.html", context)

def about(request):
    return render(request, "blog/about.html", { 'title' : 'About' })
