from dataclasses import fields
from rest_framework import serializers

from material.models import Composicion, Vagon, Bogie, Eje, Cambiador

class ComposicionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Composicion

class VagonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Vagon
        
class BogieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Bogie

class EjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Eje

class CambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cambiador