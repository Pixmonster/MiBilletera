from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("exit", views.exit, name="exit"),
    path("panel/", views.panel, name="panel"),
    path('register/', views.register, name="register"),
    path('logear/', views.logear, name='logear'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),
]