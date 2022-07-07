from dataclasses import fields
from rest_framework import serializers

from organizaciones.models import Organizacion, Diseñador, Fabricante, LicenciaFabricacion, Mantenedor
from organizaciones.models import Keeper, Operador, Aprovador, Certificador



class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Organizacion

class DiseñadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Diseñador

class FabricanteSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Fabricante

class LicenciaFabricacionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LicenciaFabricacion

class MantenedorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Mantenedor

class KeeperSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Keeper

class OperadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Operador

class AprovadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Aprovador

class CertificadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Certificador