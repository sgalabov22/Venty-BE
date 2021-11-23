from django.urls import path

from users import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.token),
    path('refresh', views.refresh_token),
    path('logout', views.revoke_token),
]
