from django.urls import path
from streaming.views import MensajeCirculacion

urlpatterns = [
    path('msg_circ', MensajeCirculacion, name = 'msg_circ'),
]