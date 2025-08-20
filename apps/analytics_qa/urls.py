from django.urls import path

from apps.analytics_qa import views


app_name = 'analytics_qa'

urlpatterns = [
    path('', views.index, name='index'),
]
