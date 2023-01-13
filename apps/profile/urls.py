from django.urls import path

from apps.profile.views import ProfileAvatarView, ChangeUserDataView, GetUserDataView

urlpatterns = [
    path('upload-avatar/', ProfileAvatarView.as_view(), name='profile'),
    path('change-user-data/', ChangeUserDataView.as_view(), name='change_user_data'),
    path('get-user-data/', GetUserDataView.as_view(), name='change_user_data'),

]
