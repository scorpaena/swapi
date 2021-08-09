from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from .serializers import StarWarsFilesSerializer
from .models import StarWarsFilesModel
from .filters import StarWarsFilesModelFilter
from .services import CSVFileProcessor


class StarWarsFileDownLoadView(generics.ListCreateAPIView):
    queryset = StarWarsFilesModel.objects.all()
    serializer_class = StarWarsFilesSerializer
    filterset_class = StarWarsFilesModelFilter


class StarWarsCSVFileView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        paginator = CursorPagination()
        csv = CSVFileProcessor()
        data = csv.read_from_csv_file(id)
        # response = paginator.get_paginated_response(data)
        return Response(data)
