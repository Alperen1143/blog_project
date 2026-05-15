from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def home(request):
    return render(request, "anasayfa/home.html")


def blog_list(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "anasayfa/blog_list.html", {"posts": posts})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "anasayfa/blog_detail.html", {"post": post})



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

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get("username_or_email")
            password = form.cleaned_data["password"]
            
            user_obj = User.objects.filter(username=username_or_email).firs()
            
            if user_obj is not None:
                user_obj = User.objects.filter(email=username_or_email).first()
                
            if user_obj is not None:
                user = authenticate(
                    request,
                    
                    username=user_obj.username,
                    password=password
                )
                
                if user is not None:
                    login(request, user)
                    messages.success(request, "Başırıyla giriş yaptınız.")
                    return redirect("home")
                else:
                    messages.error(request, "Şifre hatalı.")
            else:
                messages.error(request, "kullanıcı adı veya e-posta bulunamadı.")
    else:
        form = LoginForm()
    return render(request, "anasayfa/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("home")
