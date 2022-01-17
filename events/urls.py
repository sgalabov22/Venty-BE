from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events import views

# router = DefaultRouter()
# router.register(r'events', views.EventViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]


urlpatterns = [
    path('events', views.EventsList.as_view()),
    path('events/create', views.EventCreate.as_view()),
    path('event/<int:pk>', views.EventGetUpdateDelete.as_view()),
]
