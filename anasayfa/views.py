from datetime import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import BlogPost, Category, UserProfile
from .forms import RegisterForm, LoginForm


def home(request):
    return render(request, "anasayfa/home.html")


def blog_list(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "anasayfa/blog_list.html", {"posts": posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    posts = BlogPost.objects.filter(category=category).order_by("-created_at")
    return render(
        request,
        "anasayfa/blog_list.html",
        {
            "posts": posts,
            "category": category,
        }
    )


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "anasayfa/blog_detail.html", {"post": post})


def nasa_apod(request):
    context = {}

    if request.method == "POST":
        selected_date = request.POST.get("date", "").strip()
        context["selected_date"] = selected_date

        try:
            datetime.strptime(selected_date, "%Y-%m-%d")
        except ValueError:
            context["error_message"] = "Lütfen YYYY-MM-DD formatında geçerli bir tarih seçin."
        else:
            try:
                import requests
            except ImportError:
                context["error_message"] = "NASA isteği için requests kütüphanesi kurulmalıdır."
            else:
                try:
                    response = requests.get(
                        "https://api.nasa.gov/planetary/apod",
                        params={
                            "api_key": settings.NASA_API_KEY,
                            "date": selected_date,
                        },
                        timeout=10,
                    )
                    data = response.json()

                    if response.status_code == 200:
                        context["apod"] = {
                            "title": data.get("title"),
                            "date": data.get("date"),
                            "explanation": data.get("explanation"),
                            "url": data.get("url"),
                            "media_type": data.get("media_type"),
                            "copyright": data.get("copyright"),
                        }
                    else:
                        api_error = data.get("msg")

                        if not api_error and isinstance(data.get("error"), dict):
                            api_error = data["error"].get("message")

                        context["error_message"] = (
                            api_error
                            or "NASA API isteği başarısız oldu. Lütfen tarihi kontrol edip tekrar deneyin."
                        )
                except requests.RequestException:
                    context["error_message"] = "NASA API'ye şu anda ulaşılamıyor. Lütfen daha sonra tekrar deneyin."
                except ValueError:
                    context["error_message"] = "NASA API geçersiz bir yanıt döndürdü."

    return render(request, "anasayfa/nasa_apod.html", context)


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

            UserProfile.objects.create(
                user=user,
                full_name=full_name,
                phone=phone
            )

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
            password = form.cleaned_data.get("password")

            user_obj = User.objects.filter(username=username_or_email).first()

            if user_obj is None:
                user_obj = User.objects.filter(email=username_or_email).first()

            if user_obj is not None:
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

                if user is not None:
                    login(request, user)
                    messages.success(request, "Başarıyla giriş yaptınız.")
                    return redirect("home")
                else:
                    messages.error(request, "Şifre hatalı.")
                    return redirect("/?login_error=1")
            else:
                messages.error(request, "Kullanıcı adı veya e-posta bulunamadı.")
                return redirect("/?login_error=1")

        messages.error(request, "Giriş başarısız. Lütfen formu kontrol edin.")
        return redirect("/?login_error=1")

    return redirect("home")


def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("home")
