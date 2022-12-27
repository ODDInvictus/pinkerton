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