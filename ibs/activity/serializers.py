from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = (
          'id', 
          'name', 
          'description', 
          'date', 
          'start_time', 
          'location', 
          'organisation_id', 
          'people'
        )

    def create(self, validated_data):
      return Activity.objects.create(**validated_data)

    def update(self, instance: Activity, validated_data):
      instance.name = validated_data.get('name', instance.name)
      instance.description = validated_data.get('description', instance.description)
      instance.date = validated_data.get('date', instance.date)
      instance.start_time = validated_data.get('start_time', instance.start_time)
      instance.location = validated_data.get('location', instance.location)
      instance.organisation_id = validated_data.get('organisation', instance.organisation_id)
      instance.save()
      return instance