from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("entrar/", views.login_view, name="login"),
    path("cadastrar/", views.register_view, name="register"),
    path("sair/", views.logout_view, name="logout"),
    path("recuperar-senha/", views.password_reset_request, name="password_reset"),
    path(
        "recuperar-senha/concluido/",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "redefinir-senha/<uidb64>/<token>/",
        views.BicoPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "redefinir-senha/concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("minha-conta/", views.account_view, name="account"),
    path("minha-conta/editar/", views.account_edit, name="account_edit"),
    path(
        "minha-conta/alterar-senha/",
        views.BicoPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "minha-conta/alterar-senha/concluido/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("conversas/", views.conversations_placeholder, name="conversations"),
    path("notificacoes/", views.notifications_placeholder, name="notifications"),
]
