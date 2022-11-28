from rest_framework import serializers
from .models import Activity, Participant

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
          'id', 
          'name', 
          'description', 
          'date', 
          'start_time', 
          'location', 
          'organisation',
        )

    def create(self, validated_data):
      return Activity.objects.create(**validated_data)

    def update(self, instance: Activity, validated_data):
      instance.name = validated_data.get('name', instance.name)
      instance.description = validated_data.get('description', instance.description)
      instance.date = validated_data.get('date', instance.date)
      instance.start_time = validated_data.get('start_time', instance.start_time)
      instance.location = validated_data.get('location', instance.location)
      instance.organisation = validated_data.get('organisation', instance.organisation)
      instance.save()
      return instance


class CalendarSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()
  description = serializers.CharField()
  date = serializers.DateField()
  start_time = serializers.TimeField()
  location = serializers.CharField()
  organisation = serializers.CharField()


class ParticipantSerialzer(serializers.ModelSerializer):

  class Meta:
    model = Participant
    fields = "__all__"

    def update(self, instance: Participant, validated_data):
      instance.present = validated_data.get('present', instance.present)
      instance.save()
      return instance
