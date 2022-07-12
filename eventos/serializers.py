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


class DatosCirculacion ():
    def __init__(self, cursor):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        velocidades = []
        temperaturasA = []
        temperaturasB =[]
        aax = []
        aay = []
        aaz = []
        abx = []
        aby = []
        abz = []

        for doc in cursor:
            velocidades.append(doc["vel"])
            temperaturasA.append(doc["tempa"])
            temperaturasB.append(doc["tempb"])
            aax.extend(doc["aax"])
            aay.extend(doc["aay"])
            aaz.extend(doc["aaz"])
            abx.extend(doc["abx"])
            aby.extend(doc["aby"])
            abz.extend(doc["abz"])
        
        self.data = {'vel':velocidades, 'tempa':temperaturasA, 'tempb':temperaturasB,'aax':aax,'aay':aay,'aaz':aaz,'abx':abx,'aby':aby,'abz':abz}