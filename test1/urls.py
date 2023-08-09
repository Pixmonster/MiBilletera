from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("exit", views.exit, name="exit"),
    path("panel/", views.panel, name="panel"),
    path('register/', views.register, name="register"),
]