from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from apps.core.models import User, Post
from apps.core.forms import LoginForm, RegisterForm
from apps.core.utils_for_views import handle_invalid_form


@login_required(login_url='login')
def index(request):
    return render(request, "core/index.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # return handle_invalid_form()
            context = {
                'form': form
            }
            return render(request, 'core/login.html', context)
    else:
        context = {
            'form': LoginForm()
        }
        return render(request, 'core/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            passwordConfirmation = form.cleaned_data['passwordConfirmation']

            User.objects.create_user(username, email, password)
            
            return HttpResponseRedirect(reverse('login'))
        else:
            context = {
                'form': form
            }
            return render(request, 'core/register.html', context)
    else:
        context = {
            'form': RegisterForm
        }
        return render(request, "core/register.html", context)


@login_required(login_url='login')
def new_post(request):
    if request.method == "POST":
        Post.objects.create(user=request.user, body=request.POST['new_post'])
        data = {
            'dataKey': request.POST['new_post'] 
        }
        return JsonResponse(data)
    else:
        return HttpResponse("Post method is required to submit a new post")
