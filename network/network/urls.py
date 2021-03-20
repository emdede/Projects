
from django.urls import path
from .views import PostViewer

from . import views

urlpatterns = [
    path("", views.PostViewer.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.FollowerPostViewer.as_view(), name="following"),
    path("new", views.post, name="new_post"),
    path("like", views.like, name="like"),
    path("profile/<int:userid>", views.profile, name="profile"),
    path("profile/<int:userid>/follow", views.follow, name="follow")
]
