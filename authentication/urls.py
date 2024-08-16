from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        # auth_views.LoginView.as_view(template_name="accounts/login.html"),
        # auth_views.LoginView.as_view(),
        views.login_view,
        name="login",
    ),
    path('logout/', views.logout_view, name='logout'),
    # path('signup/', views.signup_view, name='signup_view'),
    path('change/password/', auth_views.PasswordChangeView.as_view(template_name='registration/custom_change_password.html'), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/custom_password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/custom_reset_done.html'), name='password_reset_complete'),

]