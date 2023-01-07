from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ibs.activity.models import Activity, Participant
from ibs.users.serializers import CommitteeSerializer

class ActivitySerializer(serializers.ModelSerializer):
  organisation = CommitteeSerializer(read_only=True)

  class Meta:
    model = Activity
    fields = ('__all__')

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

class ParticipantSerialzer(serializers.ModelSerializer):

  class Meta:
    model = Participant
    fields = "__all__"

    def update(self, instance: Participant, validated_data):
      instance.present = validated_data.get('present', instance.present)
      instance.save()
      return instance
