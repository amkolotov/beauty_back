from django.urls import path

from apps.profile.views import ProfileAvatarView

urlpatterns = [
    path('upload-avatar/', ProfileAvatarView.as_view(), name='profile'),
]
