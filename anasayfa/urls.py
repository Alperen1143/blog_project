from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<int:post_id>/", views.blog_detail, name="blog_detail"),
]

from django.urls import path
from . import views
urlpatterns += [
    path("register/", views.register_view, name="register"),
]