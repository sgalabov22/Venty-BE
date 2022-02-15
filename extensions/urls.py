from django.urls import path
from extensions import views


urlpatterns = [
    path('<int:pk>/extensions', views.ExtensionsGetCreate.as_view()),
    path('<int:pk>/extensions/<int:ext_id>', views.ExtensionsDetailsUpdate.as_view()),
    path('<int:pk>/extensions/<int:ext_id>/viewers', views.ExtensionsCatalogViewers.as_view()),
]