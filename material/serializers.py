from dataclasses import fields
from rest_framework import serializers
from ingenieria.models import VersionEje, VersionCambiador 

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
    version = serializers.StringRelatedField(many=False)
    fabricante = serializers.StringRelatedField(many=False)
    keeper = serializers.StringRelatedField(many=False)
    operador = serializers.StringRelatedField(many=False)
    mantenedor = serializers.StringRelatedField(many=False)
    bogie = serializers.StringRelatedField(many=False)
    vagon = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Eje

class CambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cambiador