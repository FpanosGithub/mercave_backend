from datetime import datetime, timedelta

def calcular_rango_evento (dt, rango):
    '''Función que comprueba si dt es una fecha válida'''
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    if isinstance(dt, datetime):
        print('ES FECHA')
        dt_fin = dt + timedelta(seconds=rango)
        dt_inicio = dt - timedelta(seconds=rango)
    else:
        print('NO ES FECHA')
        dt_fin = datetime.now()
        dt_inicio = dt_fin - timedelta(seconds=rango)
    
    return dt_inicio, dt_fin