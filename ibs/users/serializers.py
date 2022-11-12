from rest_framework import serializers
from .models import User, Generation, Committee, Function

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      # AbstractUser fields
      'id',
      'username',
      'first_name',
      'last_name',
      'email',
      'is_staff',
      'is_active',
      'date_joined',
      # User fields
      'nickname',
      'initials',
      'profile_picture',
      'birth_date',
      'first_drink_invited_at',
      'became_aspiring_member',
      'became_member',
      'generation',
      'bio',
      'phone_number',
    )

  def create(self, validated_data):
    return User.objects.create(**validated_data)

  def update(self, instance: User, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.email = validated_data.get('email', instance.email)
    instance.date_joined = validated_data.get('date_joined', instance.date_joined)

    instance.nickname = validated_data.get('nickname', instance.nickname)
    instance.initials = validated_data.get('initials', instance.initials)
    instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
    instance.birth_date = validated_data.get('birth_date', instance.birth_date)
    instance.became_member = validated_data.get('became_member', instance.became_member)
    instance.generation = validated_data.get('generation', instance.generation)
    instance.bio = validated_data.get('bio', instance.bio)
    instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    instance.save()
    return instance


class GenerationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Generation
    fields = (
      'id',
      'generation_number',
      'name',
      'start_date',
    )

  def create(self, validated_data):
    return Generation.objects.create(**validated_data)

  def update(self, instance: Generation, validated_data):
    instance.generation_number = validated_data.get('generation_number', instance.generation_number)
    instance.name = validated_data.get('name', instance.name)
    instance.start_date = validated_data.get('start_date', instance.start_date)
    instance.save()
    return instance


class CommitteeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Committee
    fields = (
      'id',
      'name',
      'abbreviation',
      'description',
      'created_at',
      'updated_at',
      'active',
      'admin_rights',
      'website',
      'email',
      'logo',
      'photo',
    )

  def create(self, validated_data):
    return Committee.objects.create(**validated_data)

  def update(self, instance: Committee, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.abbreviation = validated_data.get('abbreviation', instance.abbreviation)
    instance.description = validated_data.get('description', instance.description)
    instance.created_at = validated_data.get('created_at', instance.created_at)
    instance.updated_at = validated_data.get('updated_at', instance.updated_at)
    instance.active = validated_data.get('active', instance.active)
    instance.admin_rights = validated_data.get('admin_rights', instance.admin_rights)
    instance.website = validated_data.get('website', instance.website)
    instance.email = validated_data.get('email', instance.email)
    instance.logo = validated_data.get('logo', instance.logo)
    instance.photo = validated_data.get('photo', instance.photo)
    instance.save()
    return instance


class FunctionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Function
    fields = (
      'id',
      'user',
      'committee',
      'function',
      'note',
      'begin',
      'end',
      'active'
    )

  def create(self, validated_data):
    return Function.objects.create(**validated_data)

  def update(self, instance: Function, validated_data):
    instance.user = validated_data.get('user', instance.user)
    instance.committee = validated_data.get('committee', instance.committee)
    instance.function = validated_data.get('function', instance.function)
    instance.note = validated_data.get('note', instance.note)
    instance.begin = validated_data.get('begin', instance.begin)
    instance.end = validated_data.get('end', instance.end)
    instance.active = validated_data.get('active', instance.active)
    instance.save()
    return instance