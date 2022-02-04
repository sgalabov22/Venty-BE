from django.urls import path
from guests import views

urlpatterns = [
    path('<int:pk>/guests', views.EventGuestGetCreate.as_view()),
    path('<int:pk>/users', views.EventGuestCatalogUsers.as_view()),
    path('<int:pk>/guests/<int:guest_pk>', views.EventGuestUpdate.as_view()),
]
