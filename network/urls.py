
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("newpost", views.newpost, name="newpost"),
    path("page/<int:page_id>", views.displayPage, name="displayPage"),
    path("profile/<str:username>", views.displayProfile, name="displayProfile"),
]
