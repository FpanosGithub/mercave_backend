from dataclasses import fields
from rest_framework import serializers

from red_ferroviaria.models import Linea, PuntoRed

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Linea

class PuntoRedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PuntoRed