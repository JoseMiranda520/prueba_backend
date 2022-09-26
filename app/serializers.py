from rest_framework import serializers
from django.contrib.auth.models import  Group
from app.models import *
from django.contrib.auth import get_user_model
from fw.rest.serializers import BaseModelSerializer
from rest_framework_tracking.models import APIRequestLog
User = get_user_model()


class PilotSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Pilot


class PilotExcludedSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Pilot


class ProfileSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Profile


class ProfileDetailedSerializer(BaseModelSerializer):

    pilot = PilotExcludedSerializer(many=True)

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


class LinkSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Link
        #


class PublishSerializer(BaseModelSerializer):

    link_url = serializers.SerializerMethodField()
    #image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    
    def get_link_url(self, obj):
        if obj.link:
            return obj.link.link
        return None

    class Meta(BaseModelSerializer.Meta):
        model = Publish


class PublishListSerializer(PublishSerializer):
    assign_byPilot = serializers.StringRelatedField(read_only=True)
    assign_byPilot_id = serializers.SerializerMethodField()

    def get_assign_byPilot_id(self, obj):
        if obj.assign_byPilot:
            return obj.assign_byPilot.id
        return None 
        

class TagSerializer(BaseModelSerializer):	

    class Meta(BaseModelSerializer.Meta):
        model = Tag


class AlertSerializer(BaseModelSerializer):
    
    class Meta(BaseModelSerializer.Meta):
        model = Alert


class QuestionSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Question


class QuestionProductionSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Question
        exclude =  BaseModelSerializer.Meta.exclude + ('correct_option',)


class QuizSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Quiz


class QuizResultSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Quiz_result
        
        read_only_fields = ('user',)


class SaleSerializer(BaseModelSerializer):
    user = serializers.StringRelatedField()

    class Meta(BaseModelSerializer.Meta):
        model = Sale
        read_only_fields = ('value',)


class TargetSerializer(BaseModelSerializer):

    pilot_name = serializers.SerializerMethodField()

    def get_pilot_name(self, obj):
        return obj.pilot.name
    
    class Meta(BaseModelSerializer.Meta):
        model = Target


class ScriptSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Script


class ScriptListSerializer(ScriptSerializer):
    pilot = PilotSerializer (read_only=True)


class EcardSerializer(BaseModelSerializer):
    card = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta(BaseModelSerializer.Meta):
        model = Ecard


class EcardListSerializer(EcardSerializer):
    pilot = PilotSerializer (read_only=True)


class CommissionsSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Commissions


class IndicatorSerializer(BaseModelSerializer):
    
    class Meta(BaseModelSerializer.Meta):
        model = Indicator
 

class IndicatorTipSerializer(BaseModelSerializer):
    
    class Meta(BaseModelSerializer.Meta):
        model = Indicators_tip


class UserSerializer2(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'document',
            'is_superuser'
        )


class VisitSerializer(serializers.ModelSerializer):
    user = UserSerializer2 ()
    
    class Meta:
        model = APIRequestLog
        fields = (
            'id', 'requested_at', 'method', 'user'
        )


class MediaSerializer(serializers.ModelSerializer):
    '''
    Serializador de 
    '''
    class Meta:
        model = Media
        fields = '__all__'