from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BackendPagination(PageNumberPagination):

    page_size_query_param = 'page_size'
    page_size = 10

    def get_paginated_response(self, data):

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': int(self.request.query_params.get('page', 1)),
            'results': data
        })
