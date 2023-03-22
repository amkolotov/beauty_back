from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.auth_app.urls')),
    path('profile/', include('apps.profile.urls')),
    path('blog/', include('apps.blog.urls')),
    path('salon/', include('apps.salon.urls')),

    path('site/', include('api.v1.site_api.urls')),
    path('next/', include('api.v1.next_api.urls'))
]

handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
