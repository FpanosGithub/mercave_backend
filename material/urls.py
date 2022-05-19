from django.urls import path
from material.views import ListaComposiciones, DetalleComposicion, ListaVagones, DetalleVagon, ListaBogies, DetalleBogie
from material.views import ListaEjes, DetalleEje, ListaCambiadores, DetalleCambiador, ListaVersionesEjes, DetalleVersionEje, ListaVersionesCambiadores, DetalleVersionCambiador
urlpatterns = [
    path('composiciones/', ListaComposiciones.as_view(), name = 'composiciones'),
    path('composiciones/<int:pk>/', DetalleComposicion.as_view(), name = 'composicion'),
    path('vagones/', ListaVagones.as_view(), name = 'vagones'),
    path('vagones/<int:pk>/', DetalleVagon.as_view(), name = 'vagon'),
    path('bogies/', ListaBogies.as_view(), name = 'bogies'),
    path('bogies/<int:pk>/', DetalleBogie.as_view(), name = 'bogie'),
    path('ejes/', ListaEjes.as_view(), name = 'ejes'),
    path('ejes/<int:pk>/', DetalleEje.as_view(), name = 'eje'),
    path('ejes/', ListaCambiadores.as_view(), name = 'cambiadores'),
    path('ejes/<int:pk>/', DetalleCambiador.as_view(), name = 'cambiador'),
    path('ejes/', ListaVersionesEjes.as_view(), name = 'versiones_eje'),
    path('ejes/<int:pk>/', DetalleVersionEje.as_view(), name = 'version_eje'),
    path('ejes/', ListaVersionesCambiadores.as_view(), name = 'versiones_cambiador'),
    path('ejes/<int:pk>/', DetalleVersionCambiador.as_view(), name = 'version_cambiador'),
]