from rest_framework.response import Response
from .services import CSVFileProcessor


class CSVFilePagination:
    def __init__(self):
        self.csv_processor = CSVFileProcessor()
        self.page_size = 20
        self.page_query_param = "page"

    def _get_page_number(self, request):
        raw_page_number = request.query_params.get(self.page_query_param, 1)
        return int(raw_page_number)

    def _iterator_(self, page_number, id):
        object = self.csv_processor.read_from_csv_file(id)
        steps = (page_number - 1) * self.page_size
        for i in range(steps):
            next(object)
        return object

    def _iterator_with_stopiteration(self, page_number, id):
        try:
            object = self._iterator_(page_number, id)
        except StopIteration:
            return object
        return object

    def get_paginated_response(self, request, id):
        page_number = self._get_page_number(request)
        object = self._iterator_with_stopiteration(page_number, id)
        start = (page_number - 1) * self.page_size
        stop = start + self.page_size
        object_list = []
        for i in range(start, stop):
            try:
                object_list.append(next(object))
            except StopIteration:
                return Response(object_list)
        return Response(object_list)
