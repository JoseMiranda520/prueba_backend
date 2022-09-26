from abc import abstractmethod
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
import logging


class ExportModelMixinViewSet:
    resource = None

    def __init__(self, resource=None, **kwargs):
        """
        :param resource: import_export.resources.ModelResource
        """
        super().__init__(**kwargs)
        self.request = None
        self.resource = resource

    @action(detail=False, methods=['GET'])
    def export(self, request):

        queryset = self.get_queryset()

        name = queryset.model.__name__

        meta = getattr(queryset.model, '_meta')

        permission = '{}.{}'.format(meta.app_label, 'can_export')

        if not request.user.has_perm(permission):
            message = {
                'status': 'forbidden',
                'message': '{} no cuenta con permisos para exportar'.format(request.user)
            }
            return Response(message, status=403)

        try:
            if request.query_params:
                size = 1000

                params = self.request.query_params

                filters = self.get_queryset_filters(params)

                queryset = queryset.filter(**filters)
                queryset = queryset[:size][::-1]
            dataset = self.resource.export(queryset)
        except Exception as e:
            logging.exception(e)
            return HttpResponse({'error': 'Datos inváidos', 'exception': e.__str__()}, content_type='application/json')

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')

        response['Content-Disposition'] = 'attachment; filename="{}s.xls"'.format(name)
        return response

    @abstractmethod
    def get_queryset(self) -> QuerySet:
        """
        return QuerySet
        """
        pass

    @staticmethod
    def get_queryset_filters(query_params):
        params = {}

        for value in query_params.keys():
            if query_params[value]:
                params[value] = query_params.get(value)

        return params


class CreatedByMixin:
    request = None

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
