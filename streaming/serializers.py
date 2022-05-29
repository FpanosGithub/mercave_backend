from rest_framework import serializers

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Función que convierten una estructura de diccionarios anidados tipo JSON 
# en un un objeto python
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class ObjetoPy(object):
    '''Convierte la estructuar en objetos con los nombres de las keys pero son todo tipo str'''
    def __init__(self, data):
        data = dict(data)
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if isinstance(value, list):
            return [self.compute_attr_value(x) for x in value]
        elif isinstance(value, dict):
            return ObjetoPy(value)
        else:
            return value

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DRF Serializers
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Valor(serializers.Serializer):
    v1 = serializers.FloatField(default = 0.0, required = False)
    v2 = serializers.FloatField(default = 0.0, required = False)
    v3 = serializers.FloatField(default = 0.0, required = False)
    v4 = serializers.FloatField(default = 0.0, required = False)
    v5 = serializers.FloatField(default = 0.0, required = False)
    v6 = serializers.FloatField(default = 0.0, required = False)
    v7 = serializers.FloatField(default = 0.0, required = False)
    v8 = serializers.FloatField(default = 0.0, required = False)
    v9 = serializers.FloatField(default = 0.0, required = False)
    v10 = serializers.FloatField(default = 0.0, required = False)

class ValEje(serializers.Serializer):
    eje = serializers.CharField(max_length=16)
    tempa = serializers.FloatField(default = 25.0)
    tempb = serializers.FloatField(default = 25.0)
    aax = serializers.ListField()
    aay = serializers.ListField()
    aaz = serializers.ListField()
    abx = serializers.ListField()
    aby = serializers.ListField()
    aaz = serializers.ListField()

class ValidadorMensajeCirculacion(serializers.Serializer):  
    dt = serializers.DateTimeField()
    tipo_msg = serializers.CharField(max_length=5)
    vagon = serializers.CharField(max_length=16)
    lng = serializers.FloatField(default = 0)
    lat = serializers. FloatField(default = 0)
    vel = serializers. FloatField(default = 0)
    msgs_ejes = ValEje(many=True)
      

