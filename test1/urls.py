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
     path('password_reset/done/',
          auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
          name='password_reset_done'),
     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('reset/done/',
          auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
          name='password_reset_complete'),
     path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
     path('nuevo_ingreso/', views.nuevo_ingreso, name="nuevo_ingreso"),
     path('ver_ingreso/', views.ver_ingreso, name="ver_ingreso"),
     path('list_ingreso/', views.list_ingresos, name="list_ingreso"),
     path('borrar_ingreso/<int:id>', views.borrar_ingreso, name="borrar_ingreso"),
     path('editar_ingreso/<int:id>', views.editar_ingreso, name="editar_ingreso"),
     path('nuevo_gasto/', views.nuevo_gasto, name="nuevo_gasto"),
     path('ver_gasto/', views.ver_gastos, name="ver_gasto"),
     path('list_gasto/', views.list_gastos, name="list_gasto"),
     path('borrar_gasto/<int:id>/', views.borrar_gasto, name="borrar_gasto"),
     path('editar_gasto/<int:id>', views.editar_gasto, name="editar_gasto"),
     path('crear_categoria_personalizada/', views.crear_categoria_personalizada, name='crear_categoria_personalizada'),
     path('crear_fuente_personalizada/', views.crear_fuente_personalizada, name='crear_fuente_personalizada'),
     path('ver_perfil/', views.ver_perfil, name="ver_perfil")
     
]