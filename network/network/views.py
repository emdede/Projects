import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from .models import User, Post

class PostViewer(ListView):
    model = Post
    template_name = "network/index.html"
    paginate_by = 10
    ordering = ['-timestamp']


class FollowerPostViewer(ListView):
    template_name = "network/index.html"
    paginate_by = 10

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(FollowerPostViewer, self).get(*args, **kwargs)

    def get_queryset(self):
        posts = Post.objects.filter(author__in=self.request.user.following.all()).order_by("-timestamp")
        return posts


def index(request):
    p = Paginator(posts, 10)
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def post(request):
    # Create post using POST
    if request.method == "POST":
        post = Post(author=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse("index"))

    # Edit post using PUT
    elif request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data['postid'])
        if post.author != request.user:
            return HttpResponse("This post is not yours to edit.")
        post.content = data['content']
        post.save()
        return JsonResponse([post.content], safe=False)
    else: 
        return JsonResponse({"error": "Not a valid action"}, status=400)


# Profile page
def profile(request, userid):
    profile = User.objects.get(id=userid)
    return render(request, "network/profile.html", {
        "followers": profile.followers.count(),
        "user_following": request.user in profile.followers.all(),
        "following": profile.following.count(),
        "profile": profile,
        "page_obj": profile.posts.all().order_by('-timestamp')
    })


# Follow and Unfollow users
@csrf_exempt
def follow(request, userid):
    user = User.objects.get(id=userid)
    # Cannot follow yourself
    if request.user.id == userid:
        return HttpResponse("You cannot follow yourself.")
    # Cannot follow if not a user
    elif not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Follow via POST
    elif request.method == "POST":
        user.followers.add(request.user)
    # Unfollow via DELETE
    elif request.method == "DELETE":
        user.followers.remove(request.user)
    # Backup
    else:
        return HttpResponse("Something went wrong. Please visit a user's profile page in order to follow them.")
    user.save()
    return HttpResponse("Success")


# Like and Unlike posts
@csrf_exempt
def like(request):
    if request.user not in User.objects.all():
        return HttpResponse("You can only like posts when you are logged in.")
    elif request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(id=data['postid'])
        # Like post - keyword argument passed via AJAX
        if data['mode'] == "LIKE":
            post.likes.add(request.user)
        # Else Unlike
        else:
            post.likes.remove(request.user)
        post.save()
        return JsonResponse({"message":"Success", "newlikes": post.likes.count()})
    else:
        return JsonResponse({"error": "Not a valid request"})
