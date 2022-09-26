from rest_framework import serializers
from rest_framework.fields import empty


class BaseModelSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    updated_by = serializers.StringRelatedField(read_only=True)
    
    created_at = serializers.DateTimeField(read_only=True)

    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        request = self.context.get('request')

        if request:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request:
            validated_data['updated_by'] = request.user

        return super().update(instance, validated_data)

    def __init__(self, instance=None, data=empty, **kwargs):
        request = kwargs.get('request')

        # print('request is ', request)

        remove_fields = kwargs.pop('remove_fields', [])

        super().__init__(instance, data, **kwargs)

        if not isinstance(remove_fields, list):
            remove_fields = [remove_fields]

        for field_name in remove_fields:
            self.fields.pop(field_name)

    class Meta:
        exclude = ('deleted', 'deleted_at')
