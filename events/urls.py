from django.urls import path
from events import views


urlpatterns = [
    path('events', views.EventsList.as_view()),
    path('events/create', views.EventCreate.as_view()),
    path('events/<int:pk>', views.EventDetailsGetUpdateDelete.as_view()),
]
