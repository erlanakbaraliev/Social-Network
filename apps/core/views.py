from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.core.forms import LoginForm, PostForm, RegisterForm
from apps.core.models import Post, User


@login_required(login_url='login')
def index(request):
    context = {
        'form': PostForm()
    }
    return render(request, "core/index.html", context)


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
        user = request.user
        body = request.POST.get('body', False)
        Post.objects.create(user=user, body=body)

        context = {
            'message': 'Post successfully submitted!'
        }
        return JsonResponse(context)
    else:
        context = {
            'form': PostForm()
        }
        html = render_to_string("core/post.html", context, request)
        return HttpResponse(html)
