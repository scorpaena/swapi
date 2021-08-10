from rest_framework import generics
from rest_framework.views import APIView
from .pagination import CSVFilePagination
from .serializers import StarWarsFilesSerializer
from .models import StarWarsFilesModel
from .services import CSVFileProcessor


class StarWarsFileListCreateView(generics.ListCreateAPIView):
    queryset = StarWarsFilesModel.objects.all()
    serializer_class = StarWarsFilesSerializer


class StarWarsCSVFileView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        paginator = CSVFilePagination()
        response = paginator.get_paginated_response(request, id)
        return response
