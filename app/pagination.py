# -*- coding: utf-8 -*-

from rest_framework import pagination
from rest_framework.response import Response


class RestPagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size'
    page_size = 10

    def get_paginated_response(self, data):

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': int(self.request.query_params.get('page_size', 1)),
            'results': data
        })
