from django.contrib.auth.models import Group
from fw.rest.serializers import BaseModelSerializer
from rest_framework import serializers

from .models import *


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
