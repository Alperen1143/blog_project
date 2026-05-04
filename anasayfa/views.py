from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def home(request):
    return render(request, "anasayfa/home.html")


def blog_list(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "anasayfa/blog_list.html", {"posts": posts})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "anasayfa/blog_detail.html", {"post": post})