from django.urls import path
from apps.schedule import views

urlpatterns = [
    path('salon/', views.schedule_salon, name='schedule_salon'),
    path('specialist/', views.schedule_spec, name='schedule_spec'),
]

