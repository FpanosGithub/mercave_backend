import folium
from folium.plugins import MarkerCluster
import datetime

def elegir_color (dt, evento):
    if evento == 'START':
        color = 'darkgreen'
    elif evento == 'STOP':
        color = 'darkred'
    elif evento == 'NUDO':
        color = 'orange'
    elif evento == 'ALARM_TEMP' or  evento == 'ALARM_ACEL' or evento == 'ALARM_CAMB':
        color = 'red'
    elif evento == 'CAMBIO':
        color = 'purple'
    elif evento == 'INIT_MANT' or evento == 'FIN_MANT':
        color = 'pink'
    elif evento == 'CIRC':
        if dt.date() == datetime.date.today():
            color = 'blue'
        elif dt.date() == datetime.date.today() - datetime.timedelta(days=1):
            color = 'cadetblue'
        else:
            color = 'lightblue'
    else:
        color = 'gray'

    return color



def mapa_ejes(ejes):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=7, tiles = "Stamen Toner")
    mc = MarkerCluster()
    color = 'red'
    for eje in ejes:
        location = [eje.lat, eje.lng]
        html_string =  '<h5><b>EJE: <br><br>' + str(eje.codigo) + '</b></h5>' +\
                '<br><b>Bogie: </b>' + str(eje.bogie) +\
                '<br><b>Vagón: </b>' + str(eje.vagon) +\
                '<br><b>Versión: </b>' + str(eje.version) +\
                '<br><b>Fabricante: </b>' + str(eje.fabricante) +\
                '<br><b>Num. Cambios: </b>' + str(eje.num_cambios) +\
                '<br><b>Kilómetros: </b>' + str(eje.km)

        popup = folium.Popup(html = html_string, max_width=150)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color=color, icon = 'glyphicon-record'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_eje(eje, eventos):
    mapa_int = folium.Map((eje.lat, eje.lng), zoom_start=7, tiles = "Stamen Toner")
    colores_circulaciones = ['#cfd5ea','#cfd5ea','#39a78e','#14a4f4','#a80ebe','#cc0033']
    color_fabricante = 'red'
    # Pop up eje
    location = [eje.lat, eje.lng]
    html_string =  '<h5><b>EJE: <br><br>' + str(eje.codigo) + '</b></h5>' +\
                '<br><b>Bogie: </b>' + str(eje.bogie) +\
                '<br><b>Vagón: </b>' + str(eje.vagon) +\
                '<br><b>Versión: </b>' + str(eje.version) +\
                '<br><b>Fabricante: </b>' + str(eje.fabricante) +\
                '<br><b>Num. Cambios: </b>' + str(eje.num_cambios) +\
                '<br><b>Kilómetros: </b>' + str(eje.km)
    popup = folium.Popup(html = html_string, max_width=150)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color = color_fabricante, icon = 'glyphicon-record'))
    mapa_int.add_child(marker) 
    # Posiciones
    i= 0
    for evento in eventos:    
        location = [evento.lat, evento.lng]
        color = elegir_color(evento.dt, evento.evento)
        popup = str(evento.punto_red) + ' - ' + str(evento.dt) + ' - ' + str(evento.evento)
        folium.CircleMarker(
            location = location,
            radius = 6,
            popup= popup,
            color = color,
            fill = True,
            fill_color = color,
        ).add_to(mapa_int)
        i += 1

    return mapa_int._repr_html_()

def mapa_cambiadores(cambiadores):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mc = MarkerCluster()
    
    for cambiador in cambiadores:    
        location = [cambiador.lat, cambiador.lng]
        html_string =  '<h5><b>CAMBIADOR DE ANCHO: <br><br>' + str(cambiador.nombre)+ '</b></h5>' +\
                '<br><b> Versión: </b>' + str(cambiador.version) +\
                '<br><b> Fabricante: </b>' + str(cambiador.fabricante) +\
                '<br><b> Puesta en servicio: </b>' + str(cambiador.fecha_fab) +\
                '<br><b> Número de operaciones: </b>' + str(cambiador.num_cambios)       
        popup = folium.Popup(html = html_string, max_width=200)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color="darkgreen", icon = 'glyphicon-road'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_cambiador(cambiador):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mc = MarkerCluster()
     
    location = [cambiador.lat, cambiador.lng]
    html_string =  '<h5><b>CAMBIADOR DE ANCHO: <br><br>' + str(cambiador.nombre)+ '</b></h5>' +\
            '<br><b> Versión: </b>' + str(cambiador.version) +\
            '<br><b> Fabricante: </b>' + str(cambiador.fabricante) +\
            '<br><b> Puesta en servicio: </b>' + str(cambiador.fecha_fab) +\
            '<br><b> Número de operaciones: </b>' + str(cambiador.num_cambios)       
    popup = folium.Popup(html = html_string, max_width=200)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color="darkgreen", icon = 'glyphicon-road'))
    mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_bogies(bogies):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mc = MarkerCluster()
    color = 'darkblue'
    for bogie in bogies:    
        location = [bogie.lat, bogie.lng]
        html_string =  '<h5><b>BOGIE: <br><br>' + str(bogie.codigo)+ '</b></h5>' +\
                '<br><b> Tipo:' + str(bogie.tipo) + '</b>' +\
                '<br><b> Operador: </b>' + str(bogie.operador)  
        popup = folium.Popup(html = html_string, max_width=200)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color, icon = 'glyphicon-minus'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_bogie(bogie):
    mapa_int = folium.Map((bogie.lat, bogie.lng), zoom_start=6)
    # Pop up eje
    location = [bogie.lat, bogie.lng]
    color_operador = 'darkblue'
    html_string =  '<h5><b>BOGIE: <br><br>' + str(bogie.codigo)+ '</b></h5>'  
    popup = folium.Popup(html = html_string, max_width=150)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color_operador, icon = 'glyphicon-minus'))
    mapa_int.add_child(marker) 

    return mapa_int._repr_html_()

def mapa_vagones(vagones):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mc = MarkerCluster()
    color = 'darkblue'
    for vagon in vagones:    
        location = [vagon.lat, vagon.lng]
        html_string =  '<h5><b>VAGÓN: <br><br>' + str(vagon.codigo)+ '</b></h5>' +\
                '<br><b> Tipo:' + str(vagon.tipo) + '</b>' +\
                '<br><b> Descripción:' + str(vagon.descripcion) + '</b>' +\
                '<br><b> Operador: </b>' + str(vagon.operador)  
        popup = folium.Popup(html = html_string, max_width=200)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color, icon = 'glyphicon-chevron-right'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_vagon(vagon, circulaciones):
    mapa_int = folium.Map((vagon.lat, vagon.lng), zoom_start=6)
    # Pop up eje
    location = [vagon.lat, vagon.lng]
    color_operador = 'darkblue'
    html_string =  '<h5><b>VAGÓN: <br><br>' + str(vagon.codigo)+ '</b></h5>'  
    popup = folium.Popup(html = html_string, max_width=150)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color_operador, icon = 'glyphicon-chevron-right'))
    mapa_int.add_child(marker) 

    return mapa_int._repr_html_()

def mapa_composiciones(composiciones):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mc = MarkerCluster()
    color = 'darkblue'
    for composicion in composiciones:    
        location = [composicion.lat, composicion.lng]
        html_string =  '<h5><b>COMPOSICIÓN: <br><br>' + str(composicion.codigo)+ '</b></h5>' +\
                '<br><b>' + str(composicion.descripcion) + '</b>' +\
                '<br><b> Operador: </b>' + str(composicion.operador)  
        popup = folium.Popup(html = html_string, max_width=200)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color, icon = 'glyphicon-asterisk'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_composicion(composicion, circulaciones):
    mapa_int = folium.Map((composicion.lat, composicion.lng), zoom_start=6)
    # Pop up eje
    location = [composicion.lat, composicion.lng]
    color_operador = 'darkblue'
    html_string =  '<h5><b>COMPOSICIÓN: <br><br>' + str(composicion.codigo)+ '</b></h5>' +\
            '<br><b>' + str(composicion.descripcion) + '</b>' +\
            '<br><b> Operador: </b>' + str(composicion.operador)  
    popup = folium.Popup(html = html_string, max_width=150)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color_operador, icon = 'glyphicon-asterisk'))
    mapa_int.add_child(marker) 

    # Posiciones
    colores_circulaciones = ['#cfd5ea','#39a78e','#14a4f4','#a80ebe','#cc0033']
    i= 0
    for circulacion in circulaciones:    
        location = [circulacion.pinicio.puntored.lat, circulacion.pinicio.puntored.lng]
        color = color = colores_circulaciones[i]
        popup = str(circulacion.pinicio.puntored.descripcion) + ' - ' + str(circulacion.dia)
        folium.CircleMarker(
            location = location,
            radius = 10,
            popup= popup,
            color=color,
            fill = True,
            fill_color = color,
        ).add_to(mapa_int)
        i += 1

    return mapa_int._repr_html_()
    
def mapa_cambios(cambios):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=5)
    mc = MarkerCluster()
    
    for cambio in cambios:    
        location = [cambio.cambiador.lat, cambio.cambiador.lng]
        html_string =  '<h5><b>CAMBIO DE EJE: <br><br>' + str(cambio.eje.codigo) + '</b></h5>' +\
                '<br><b>Cambiador : </b>' + str(cambio.cambiador.nombre)+\
                '<br><b> fecha: </b>' + str(cambio.inicio) +\
                '<br><b> sentido: </b>' + str(cambio.sentido)  
        popup = folium.Popup(html = html_string, max_width=200)
        marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color="blue", ICON = 'plus'))
        mc.add_child(marker)
    mapa.add_child(mc)    

    return mapa._repr_html_()

def mapa_alarma(alarma):
    mapa_int = folium.Map((alarma.lat, alarma.lng), zoom_start=5)
    # Pop up alarma
    location = [alarma.lat, alarma.lng]
    color_alarmas = 'red'
    html_string =  '<h5><b>Alarma: <br><br>' + str(alarma.fecha_hora)+ '</b></h5>'  
    popup = folium.Popup(html = html_string, max_width=150)
    marker = folium.Marker(location = location, popup = popup, icon = folium.Icon(color= color_alarmas, icon = 'glyphicon-volume-up'))
    mapa_int.add_child(marker) 

    return mapa_int._repr_html_()

def mapa_posicionar(puntos_red):
    mapa = folium.Map((39.8000, -2.9019), zoom_start=6)
    mapa.add_child(folium.LatLngPopup())
    
    for punto_red in puntos_red:    
        location = [punto_red.lat, punto_red.lng]
        popup = str(punto_red.codigo + '(' + str(punto_red.lng) + ',' + str(punto_red.lat) + ')')
        folium.CircleMarker(
            location = location,
            radius = 10,
            popup= popup,
            color='red',
            fill = True,
            fill_color = 'grey',
        ).add_to(mapa)
      
    return mapa._repr_html_()
