from django.contrib.auth.models import User, Group
from rest_framework import serializers

from userportal.models import AudioUploadModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UploadAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioUploadModel
        fields = ['title', 'audio']