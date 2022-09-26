from django.contrib.auth.models import Group
from fw.rest.serializers import BaseModelSerializer
from rest_framework import serializers

from .models import *


class AsignarViajeSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField()
    class Meta:
        model = Viajes
        fields = (
            'id',
            'placa_vehiculo',
            'estado'
        )

    def validate(self, data):
        if ('id' not in data or 'placa_vehiculo' not in data or 'estado' not in data):
            raise serializers.ValidationError(""" los campos "id", "placa_vehiculo" y "estado" son requeridos""")
        return data


class ViajesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Viajes
        fields = '__all__'



class PilotSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Pilot


class ProfileSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Profile


class ProfileDetailedSerializer(BaseModelSerializer):
    pilot = PilotSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'is_active',
            'profile',
            'document',
            'is_superuser'
        )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class GroupNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
