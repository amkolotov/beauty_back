from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth_app.views import RegisterView, TokenObtainPairFromCodeView, ResetPasswordView, \
    TokenObtainPairFromLoginView, ResetPasswordSetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('code/', TokenObtainPairFromCodeView.as_view(), name='send_code'),
    path('token/', TokenObtainPairFromLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-set/', ResetPasswordSetView.as_view(), name='reset_password_set'),
]
