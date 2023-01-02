from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth_app.views import RegisterView, TokenObtainPairFromCodeView, ResetPasswordView, \
    TokenObtainPairFromLoginView, ChangeUserDataView, GetUserDataView, ResetPasswordSetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('code/', TokenObtainPairFromCodeView.as_view(), name='send_code'),
    path('token/', TokenObtainPairFromLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-set/', ResetPasswordSetView.as_view(), name='reset_password_set'),
    path('change-user-data/', ChangeUserDataView.as_view(), name='change_user_data'),
    path('get-user-data/', GetUserDataView.as_view(), name='change_user_data'),
]
