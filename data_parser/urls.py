from django.urls import path
from .views import StarWarsFileDownLoadView, StarWarsCSVFileView

urlpatterns = [
    path("files/", StarWarsFileDownLoadView.as_view()),
    path("files/csv/<int:pk>", StarWarsCSVFileView.as_view()),
]
