from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row
from bokeh.models import BoxAnnotation
from pymongo import MongoClient


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def plotear_velocidad_eje(eje):
    '''Devuelve gráfica de las 40 últimas velocidades enviadas (40 últimos segundos?)
        Las cogemos de Mongo.
    '''
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Mongo

    # inicializamos MONGO_DB para guardar mensajes de vagón y ejes
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_mongo = client.mercave_mongo
    cursor_vel = mercave_mongo.circulaciones_ejes.find(
        {'eje':eje},{'vel':1, "_id": 0}
    ).limit(30).sort([('dt',-1)])



    x = list(range(10))
    vel = list(cursor_vel)
    
    p1 = figure(title="Velocidad", height = 300)
    p1.line(x, vel, legend_label="km/h", line_width=2)
    p1.toolbar_location = None
    
    return file_html(p1, CDN, "Velocidad")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def plotear_alarma_circulacion(alarma):
    x = list(range(10))
    ax = [alarma.ax0, alarma.ax1, alarma.ax2, alarma.ax3, alarma.ax4, alarma.ax5, alarma.ax6, alarma.ax7, alarma.ax8, alarma.ax9]
    ay = [alarma.ay0, alarma.ay1, alarma.ay2, alarma.ay3, alarma.ay4, alarma.ay5, alarma.ay6, alarma.ay7, alarma.ay8, alarma.ay9]
    az = [alarma.az0, alarma.az1, alarma.az2, alarma.az3, alarma.az4, alarma.az5, alarma.az6, alarma.az7, alarma.az8, alarma.az9]
    temp = [alarma.t0, alarma.t1, alarma.t2, alarma.t3, alarma.t4, alarma.t5, alarma.t6, alarma.t7, alarma.t8, alarma.t9]
    
    mid_box_a = BoxAnnotation(bottom=-2, top=2, fill_alpha=0.2, fill_color="#009E73")
    mid_box_t = BoxAnnotation(bottom=33, top=45, fill_alpha=0.2, fill_color="#009E73")
    
    p1 = figure(title="Aceleraciones Verticales", x_axis_label='p.k', y_range = (-8, 8), height = 300)
    p2 = figure(title="Aceleraciones Laterales", x_axis_label='p.k', y_range = (-8, 8), height = 300)
    p3 = figure(title="Aceleraciones y Deceleraciones", x_axis_label='p.k', y_range = (-12,12), height = 300)
    p4 = figure(title="Temperatura", x_axis_label='x',y_range = (-8, 48), height = 300)

    p1.line(x, ax, legend_label="ax m/s^2", line_width=2)
    p2.line(x, ay, legend_label="ay m/s^2", color="blue", line_width=2)
    p3.line(x, az, legend_label="az m/s^2", color="red", line_width=2)   
    p4.line(x, temp, legend_label="temp ºC", color="red", line_width=2)  
    p1.toolbar_location = None
    p2.toolbar_location = None
    p3.toolbar_location = None
    p4.toolbar_location = None
    p1.add_layout(mid_box_a)
    p2.add_layout(mid_box_a)
    p3.add_layout(mid_box_a)
    p4.add_layout(mid_box_t)
    
    r = row([p1, p2, p3, p4], sizing_mode="stretch_width")
    return file_html(r, CDN, "Alarma")
  #  return file_html(p1, CDN, "Alarma"), file_html(p2, CDN, "Alarma"), file_html(p3, CDN, "Alarma"), file_html(p4, CDN, "Alarma")
def plotear_cambios(cambios):
    fdM =[] 
    ddM =[]
    fcM =[] 
    dcM =[]
    fem =[] 
    dem =[]
    for cambio in cambios:
        fdM.append(cambio.fdaM)
        fdM.append(cambio.fdbM)
        ddM.append(cambio.ddaM)
        ddM.append(cambio.ddbM)
        fcM.append(cambio.fcaM)
        fcM.append(cambio.fcbM)
        dcM.append(cambio.dcaM)
        dcM.append(cambio.dcbM)
        fem.append(cambio.feam)
        fem.append(cambio.febm)
        dem.append(cambio.deam)
        dem.append(cambio.debm)

    p1 = figure(title="Fuerza Descerrojamiento", x_axis_label='mm de desplazamiento de disco',)
    p1.circle(ddM, fdM, legend_label="fd Kn", color="red", size=12)
    p1.toolbar_location = None
    
    p2 = figure(title="Fuerza Cambio Rueda", x_axis_label='mm de desplazamiento de rueda',)
    p2.circle(dcM, fcM, legend_label="fc Kn", color="green", size=12)
    p2.toolbar_location = None
    
    p3 = figure(title="Fuerza Encerrojamiento", x_axis_label='mm de desplazamiento de disco',)
    p3.circle(dem, fem, legend_label="fd Kn", color="blue", size=12)
    p3.toolbar_location = None
    
    # r = row([p1, p2, p3], sizing_mode="stretch_width")
    return file_html(p1, CDN, "Cambios"), file_html(p2, CDN, "Cambios"), file_html(p3, CDN, "Cambios")