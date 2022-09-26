from django_filters import FilterSet

from .models import *


class PilotFilter(FilterSet):
    """
    Filtro para Pilot
    """

    class Meta:
        model = Pilot
        fields = {
            'name': ['icontains', 'exact'],
        }


class ProfileFilter(FilterSet):
    """
    Filtro para Profile
    """

    class Meta:
        model = Profile
        fields = {
            'user': ['exact'],
            'pilot': ['icontains', 'exact'],
            'notepad': ['icontains', 'exact'],
        }


class UserFilter(FilterSet):
    """
    Filtro para Script
    """

    class Meta:
        model = User
        fields = {
            'username': ['exact'],
            'profile__pilot': ['exact'],
        }
