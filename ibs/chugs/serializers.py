from rest_framework import serializers
from .models import Strafbak, Anytimer, Chug

class StrafbakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strafbak
        fields = (
          'id', 
          'receiver', 
          'giver', 
          'reason', 
          'date'
        )

    def create(self, validated_data):
      return Strafbak.objects.create(**validated_data)

    # def to_representation(self, instance):
    #     rep = super(StrafbakSerializer, self).to_representation(instance)
    #     rep['receiver'] = instance.receiver.username
    #     rep['giver'] = instance.giver.username
    #     return rep

class ChugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chug
        fields = (
          'id', 
          'user', 
          'date', 
          'time'
        )

    def create(self, validated_data):
      return Chug.objects.create(**validated_data)