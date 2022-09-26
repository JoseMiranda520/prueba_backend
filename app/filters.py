'''
Filtros de de app
'''
from django_filters import rest_framework as filters
from .models import *


from rest_framework_tracking.models import APIRequestLog

class PilotFilter(filters.FilterSet):
    '''
    Filtro para Pilot
    '''

    class Meta:
        model = Pilot
        fields = {
            'name': ['icontains', 'exact'],
        }

"""
class FaqFilter(filters.FilterSet):
    '''
    Filtro para Faq
    '''

    class Meta:
        model = Faq
        fields = {
            'question': ['icontains', 'exact'],
            'reply': ['icontains', 'exact'],
        }"""


class LinkFilter(filters.FilterSet):
    '''
    Filtro para Link
    '''
    
    class Meta:
        model = Link
        fields = {
            'title': ['icontains', 'exact']
        }


class TagFilter(filters.FilterSet):
    '''
    Filtro para Tag
    '''
    
    class Meta:
        model = Tag
        fields = {
            'name': ['icontains', 'exact']
        }


class PublishFilter(filters.FilterSet):
    '''
    Filtro para Publish
    '''

    class Meta:
        model = Publish
        fields = {
            'title': ['icontains', 'exact'],
            'short_description': ['icontains', 'exact'],
            'description': ['icontains', 'exact'],
            'tags': ['exact',],
            'tags__name': ['icontains',],
            'link': ['exact'],
            'assign_byPilot': ['exact']
        }


class AlertFilter(filters.FilterSet):
    '''
    Filtro para Alert
    '''

    class Meta:
        model = Alert
        fields = {
            'name': ['icontains', 'exact'],
            'content': ['icontains', 'exact'],
            'pilot': ['icontains', 'exact'],
            'status': ['icontains','exact'],
            'created_by': [ 'exact'],
            'date': ['exact'],
        }


class QuestionFilter(filters.FilterSet):
    '''
    Filtro para Question
    '''

    class Meta:
        model = Question
        fields = {
            'texto': ['icontains', 'exact'],
            'multiple': ['icontains', 'exact'],
            'option_list': ['icontains', 'exact'],
            'correct_option': ['icontains','exact'],
        }


class QuizFilter(filters.FilterSet):
    '''
    Filtro para Quiz
    '''

    class Meta:
        model = Quiz
        fields = {
            'name': ['icontains', 'exact'],
            'questions': ['icontains', 'exact'],
            'assign_byPilot': ['exact'],
        }


class QuizResultFilter(filters.FilterSet):
    '''
    Filtro para QuizResult
    '''

    class Meta:
        model = Quiz_result
        fields = {
            'quiz': ['exact'],
            'pilot': ['exact'],
            'user': ['exact'],
            'result': ['gt', 'lt']
        }


class ProfileFilter(filters.FilterSet):
    '''
    Filtro para Profile
    '''

    class Meta:
        model = Profile
        fields = {
            'user': ['exact'],
            # 'bio': ['icontains', 'exact'],
            # 'birth_date': ['icontains', 'exact'],
            'pilot': ['icontains', 'exact'],
            'notepad': ['icontains', 'exact'],
        }


class ScriptFilter(filters.FilterSet):
    '''
    Filtro para Script
    '''

    class Meta:
        model = Script
        fields = {
            'title': ['icontains', 'exact'],
            'text': ['icontains'],
            'pilot': ['exact'],
        }


class UserFilter(filters.FilterSet):
    '''
    Filtro para Script
    '''

    class Meta:
        model = User
        fields = {
            'username': ['exact']
        }


class APIRequestLogFilter(filters.FilterSet):
    '''
    Filtro para Script
    '''
    class Meta: 
        model = APIRequestLog
        fields = {
            'requested_at': ['icontains', 'exact']
        }


class MediaFilter(filters.FilterSet):
    '''
    Filtro para Media
    '''
    class Meta:
        model = Media
        fields = {
            'title': ['icontains', 'exact'],
        }


class EcardFilter(filters.FilterSet):
    '''
    Filtro para Ecard
    '''
    class Meta:
        model = Ecard
        fields = {
            'title': ['icontains', 'exact'],
            'id': ['icontains', 'exact'],
            'detail': ['icontains', 'exact'],
            'link': ['icontains', 'exact'],
            'pilot': ['exact'],
        }


class ScriptFilter(filters.FilterSet):
    '''
    Filtro para Script
    '''
    class Meta:
        model = Script
        fields = {
            'title': ['icontains', 'exact'],
            'text': ['icontains', 'exact'],
            'pilot': ['exact'],
        }