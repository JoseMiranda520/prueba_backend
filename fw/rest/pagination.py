from django.conf import Settings
from rest_framework import pagination
from rest_framework.response import Response


class RestPagination(pagination.PageNumberPagination):

    page_size_query_param = getattr(Settings, 'PAGE_PARAM_NAME', 'page_size')
    page_size = getattr(Settings, 'PAGINATION_SIZE', 10)

    def get_paginated_response(self, data):

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': int(self.request.query_params.get('page', 1)),
            'results': data
        })
