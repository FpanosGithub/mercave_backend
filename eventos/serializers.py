from dataclasses import fields
from rest_framework import serializers
from eventos.models import Cambio, EventoVagon, Mantenimiento, AlarmaCambio, AlarmaTemp, AlarmaAceleracion, EventoEje, EventoVagon

class CambioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cambio

class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Mantenimiento

class AlarmaCambioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AlarmaCambio

class AlarmaTempSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AlarmaTemp

class AlarmaAceleracionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AlarmaAceleracion

class EventoEjeSerializer(serializers.ModelSerializer):
    en_bogie = serializers.StringRelatedField(many=False)
    en_vagon = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = EventoEje

class EventoVagonSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = EventoVagon