from django.urls import path

from users import views

urlpatterns = [
    path('register', views.register),
    path('login', views.token),
    path('refresh', views.refresh_token),
    path('logout', views.revoke_token),
]