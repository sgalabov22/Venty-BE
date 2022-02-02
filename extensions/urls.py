from django.urls import path
from extensions import views


urlpatterns = [
    path('<int:pk>/extensions', views.ChecklistCatalog.as_view()),
]