
from rest_framework import serializers
from project_db.models import Users, Organizations, Events


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'telegram', 'role', 'password', 'is_verified']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = ['id', 'name', 'description', 'contact_email', 'website_url', 'is_verified']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'organization', 'title', 'start_time', 'end_time', 'description']