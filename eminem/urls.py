from django.contrib import admin
from django.urls import path
from eminem import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.upload_image, name='report'),
    path('aboutUS/', views.aboutUS, name='aboutUS'),
    path('result/', views.result, name='result'),
]