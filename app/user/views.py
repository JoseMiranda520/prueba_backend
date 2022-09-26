from app import user
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from fw.rest.views import ExportModelMixinViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.views import APIView

from .filters import UserFilter, ProfileFilter, PilotFilter
from .models import *
from .resources import UserResource
from .serializers import *
import json




class UserViewSet(viewsets.ModelViewSet, ExportModelMixinViewSet):
    queryset = User.objects.all()
    resource = UserResource()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def sac_off(self, request):
        queryset = User.objects.filter(profile__pilot=30)
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupNameViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupNameSerializer

    def list(self, request, *args, **kwargs):
        try:
            document = request.GET['document']
            user = User.objects.filter(document=document)
            for element in user:
                usuario = element  
            serializer_context = {
                'request': request,
            }
            serializer_class = GroupNameSerializer(usuario.groups, many=True)
            return Response(serializer_class.data)
        except Exception:
            return Response({'msg': 'Documento no ingresado o no válido'})
        

class PilotViewSet(viewsets.ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    def list(self, request):
        if request.GET.get('nopaginate'):
            query = Pilot.objects.filter(active=True)
            serializer_coverage = PilotSerializer(query, many=True)
            self.pagination_class = None
            return Response(serializer_coverage.data)
        return super().list(request)

    filter_class = PilotFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def all(self, request):
        queryset = Pilot.objects.filter(active=True)
        serializer = PilotSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    filter_class = ProfileFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    @action(detail=False, methods=['GET'])
    def retrieve_profile(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'No tienes permisos para hacer esta consulta.'})
        user = self.request.query_params.get('user', None)
        if user:

            try:
                profile = Profile.objects.get(user__username=user)
                profile = ProfileDetailedSerializer(profile, context={'request': request}).data
                return Response({'profile': profile})
            except Profile.DoesNotExist:
                return Response({'detail': 'No existe este perfil.'})

        return Response({'detail': 'Se debe indicar el asesor a consultar.'})

    @action(detail=False, methods=['GET'])
    def get_my_profile(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'detail': 'No existe este perfil.'})

        if profile.pilot:
            pilots = PilotSerializer(profile.pilot, many=True).data
        else:
            pilots = None

        profile = ProfileSerializer(profile, context={'request': request}).data

        return Response({'profile': profile, 'pilots': pilots})

    @action(detail=True, methods=['POST'])
    def set_avatar(self, request, pk):
        try:
            if 'file' in request.FILES:
                profile = Profile.objects.get(id=pk)
                avatar = request.FILES['file']
                profile.avatar = avatar
                profile.save()
            else:
                return Response({'detail': 'No se ha agregado ningún archivo'})
            return Response({
                'detail': 'success',
                'new_route': str(profile.avatar.url)
            })
        except ValidationError:
            return Response({'detail': 'Formato inválido'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class Login(LoggingMixin, ObtainJSONWebToken):

    serializer_class = JSONWebTokenSerializer

    def handle_log(self):
        # Do some stuff before saving.
        if self.log['status_code'] == 200:
            resp = json.loads(self.log['response'])
            self.log['user_id'] = resp['user']['id']
            #self.log['username_persistent'] = resp['user']['username']
            super(Login, self).handle_log()


class Viajes(viewsets.ModelViewSet):
    """
    vista para ingresar y aceptar viajes
    @author: Jose Javier Miranda
    """
    queryset = Viajes.objects.all()
    serializer_class = ViajesSerializer

    
    def create(self, request, *args, **kwargs):

        new_serializer = ViajesSerializer(data=request.data)
        if new_serializer.is_valid():
            viaje = new_serializer.save()
            return Response({'msj':'viaje solicitado', 'id':viaje.pk}, status=status.HTTP_201_CREATED)
        return Response(new_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['PUT'], url_path='edit')
    def asignar_viaje(self, request, *args, **kwargs):

        new_serializer = AsignarViajeSerializer(data=request.data)
        if new_serializer.is_valid():
            id = new_serializer.data.get('id')
            setquery = Viajes.objects.filter(pk=id, estado='solicitado').update(**new_serializer.validated_data)
            return Response(setquery.values(), status=status.HTTP_201_CREATED)
        return Response(new_serializer.errors,status=status.HTTP_400_BAD_REQUEST)