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
    path('events/<int:pk>', views.EventDetailsGetUpdateDelete.as_view()),
    path('events/<int:pk>/guests', views.EventGuestGetCreate.as_view()),
    path('events/<int:pk>/users', views.EventGuestCatalogUsers.as_view()),
    path('events/<int:pk>/guests/<int:guest_pk>', views.EventGuestUpdate.as_view()),
]
