from django.urls import path
from .views import StarWarsFileListCreateView, StarWarsCSVFileView

urlpatterns = [
    path("files/", StarWarsFileListCreateView.as_view()),
    path("files/csv/<int:pk>/", StarWarsCSVFileView.as_view()),
]
