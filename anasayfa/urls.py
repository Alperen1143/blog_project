from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<int:post_id>/", views.blog_detail, name="blog_detail"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

urlpatterns += [
    path("register/", views.register_view, name="register"),
]
