import random
from database import guardar_equipo, guardar_partido, obtener_equipos, obtener_partidos

def armar_grupos_aleatorios(nombres_equipos, cant_grupos=2):
    random.shuffle(nombres_equipos)
    grupos = {}
    nombres_grupos = [f"Grupo {chr(65 + i)}" for i in range(cant_grupos)]
    
    for i, nombre in enumerate(nombres_equipos):
        grupo_asignado = nombres_grupos[i % cant_grupos]
        id_eq = guardar_equipo(nombre, grupo_asignado)
        if grupo_asignado not in grupos:
            grupos[grupo_asignado] = []
        grupos[grupo_asignado].append({'id': id_eq, 'nombre': nombre})
        
    return grupos

def generar_fixture_todos_contra_todos(grupos):
    for grupo, equipos in grupos.items():
        n = len(equipos)
        for i in range(n):
            for j in range(i + 1, n):
                guardar_partido(equipos[i]['id'], equipos[j]['id'])

def calcular_tabla_posiciones():
    equipos = obtener_equipos()
    partidos = obtener_partidos()

    tabla = {}
    for eq in equipos:
        tabla[eq['nombre']] = {
            'grupo': eq['grupo'],
            'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
            'gf': 0, 'gc': 0, 'dg': 0, 'pts': 0
        }

    for p in partidos:
        if p['jugado']:
            loc, vis = p['local'], p['visitante']
            gl, gv = p['goles_local'], p['goles_visitante']

            tabla[loc]['pj'] += 1
            tabla[vis]['pj'] += 1
            tabla[loc]['gf'] += gl
            tabla[vis]['gf'] += gv
            tabla[loc]['gc'] += gv
            tabla[vis]['gc'] += gl

            if gl > gv:
                tabla[loc]['pg'] += 1
                tabla[loc]['pts'] += 3
                tabla[vis]['pp'] += 1
            elif gv > gl:
                tabla[vis]['pg'] += 1
                tabla[vis]['pts'] += 3
                tabla[loc]['pp'] += 1
            else:
                tabla[loc]['pe'] += 1
                tabla[vis]['pe'] += 1
                tabla[loc]['pts'] += 1
                tabla[vis]['pts'] += 1

            tabla[loc]['dg'] = tabla[loc]['gf'] - tabla[loc]['gc']
            tabla[vis]['dg'] = tabla[vis]['gf'] - tabla[vis]['gc']

    return tabla
