from django.urls import path

from users import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('refresh', views.refresh_token),
    # path('logout', views.LogoutView.as_view()),
]
