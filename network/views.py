from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post, Follow


def index(request):
    return render(request, "network/index.html")


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

def newpost(request):
    if(request.method == "POST"):
        post = Post(user=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({"error": "newpost url is accessible only using POST method"})
    

def displayPage(request, page_id):
    allposts = Post.objects.all().order_by('-timedate')  # Order posts if necessary
    paginator = Paginator(allposts, 4)  # Show 10 posts per page

    try:
        page = paginator.page(page_id)
    except:
        return JsonResponse({"error": "Invalid page number"}, status=400)

    posts_list = [
        {
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timedate": post.timedate.strftime("%Y-%m-%d %H:%M:%S"),  # Format date
        }
        for post in page.object_list
    ]

    return JsonResponse({
        "posts": posts_list,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "current_page": page.number,
        "total_pages": paginator.num_pages,
    })

def displayProfile(request, username):
    user = User.objects.get(username=username)
    allposts = Post.objects.filter(user=user).order_by('-timedate')

    # Retrieve the page number from query parameters, defaulting to 1 if not provided.
    page = request.GET.get('page', 1)
    POSTS_PER_PAGE = 4  # or any number that suits your needs

    paginator = Paginator(allposts, POSTS_PER_PAGE)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    posts_list = [
        {
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timedate": post.timedate.strftime("%Y-%m-%d %H:%M:%S"),  # Format date
        }
        for post in page_obj
    ]

    user = User.objects.get(username=username)
    followers = Follow.objects.filter(followed=user) # Follow.objects.filter(followed=zsolt) => list of users where followed is zsolt = list of zsolts followers
    followers_list = [
        {
            "followers": follow.follower.username
        }
        for follow in followers
    ]
    
    followed = Follow.objects.filter(follower=user) # Follow.objects.filter(follower=zsolt) => list of users where follower is zsolt = how many zsolt has followed
    followed_list = [
        {
            "followed": follow.followed.username
        }
        for follow in followed
    ]

    return JsonResponse({
        "posts": posts_list,
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "followed": followed_list,
        "followers": followers_list
    })