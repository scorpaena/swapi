from rest_framework.response import Response
from .services import StarWarsCSVFileProcessor


class StarWarsCSVFileIteration:
    def __init__(self):
        self.csv_processor = StarWarsCSVFileProcessor()

    def _object_iterator(self, page_number, page_size, id):
        object = self.csv_processor.read_from_csv_file(id)
        steps = (page_number - 1) * page_size
        for i in range(steps):
            next(object)
        return object


class StarWarsCSVFilePagination:
    def __init__(self):
        self.iterator = StarWarsCSVFileIteration()
        self.page_size = 20
        self.page_query_param = "page"

    def _get_page_number(self, request):
        raw_page_number = request.query_params.get(self.page_query_param, 1)
        return int(raw_page_number)

    def get_paginated_response(self, request, id):
        page_number = self._get_page_number(request)
        page_size = self.page_size
        object = self.iterator._object_iterator(page_number, page_size, id)
        object_list = []
        for i in range(self.page_size):
            try:
                object_list.append(next(object))
            except StopIteration:
                return Response(object_list)
        return Response(object_list)
