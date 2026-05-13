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

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get("full_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            
            name_parts = full_name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserProfile.objects.create(user=user, phone=phone)
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            return redirect("home")
        else:
           messages.error(request, "Kayıt başarısız! Lütfen formu kontrol edin.")
        
    else:
        form = RegisterForm()
    return render(request, "anasayfa/register.html", {"form": form})
        
