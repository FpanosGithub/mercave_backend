from dataclasses import fields
from rest_framework import serializers

from ingenieria.models import VersionEje, VersionCambiador

class VersionEjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = VersionEje

class VersionCambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = VersionCambiador