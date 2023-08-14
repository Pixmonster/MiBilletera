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
     path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name="reset_password"),
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
     path('nuevo_ingreso/', views.nuevo_ingreso, name="nuevo_ingreso"),

]