from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Авторизация
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    # Выход
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    # Регистрация
    path('signup/', views.SignUp.as_view(), name='signup'),
    # Восстановление пароля
    path('password_reset/',
         PasswordResetView.as_view(),
         name='password_reset_form'),
    # Смена пароля
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change.html'),
         name='password_change'),
    # Пароль изменён
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
    # Восстановление пароля
    path('password_reset_form/',
         PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset_form'),
    # Восстановление пароля завершено
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
