import os
import json
import hashlib
import sys

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ruta_json = os.path.join(base_dir, 'datos.json')

datos_inicio = {
    'configuracion': {
        'nombre_colegio': 'Colegio',
        'escala_maxima': 20,
        'nota_aprobatoria': 10
    },
    'periodos': ['2026-2027'],
    'usuarios': [],
    'estudiantes': [],
    'secciones': ['A', 'B'],
    'materias': [],
    'calificaciones': [],
}


def cargar_datos():
    if not os.path.exists(ruta_json):
        guardar_datos(datos_inicio)
        return json.loads(json.dumps(datos_inicio))
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    carpeta = os.path.dirname(ruta_json)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta_json, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def encriptar(password):
    return hashlib.sha256(password.encode()).hexdigest()


def crear_admin():
    datos = cargar_datos()
    if len(datos['usuarios']) == 0:
        datos['usuarios'].append({
            'username': 'admin',
            'password_hash': encriptar('1234'),
            'rol': 'Admin'
        })
        guardar_datos(datos)


def registrar_usuario(username, password, rol):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['username'] == username:
            return False
    datos['usuarios'].append({
        'username': username,
        'password_hash': encriptar(password),
        'rol': rol
    })
    guardar_datos(datos)
    return True


def validar_login(username, password):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['username'] == username and usuario['password_hash'] == encriptar(password):
            return True
    return False


def obtener_periodos():
    datos = cargar_datos()
    if 'periodos' not in datos or len(datos['periodos']) == 0:
        datos['periodos'] = ['2026-2027']
        guardar_datos(datos)
    return datos['periodos']


def agregar_periodo(nombre):
    datos = cargar_datos()
    if 'periodos' not in datos:
        datos['periodos'] = ['2026-2027']
    limpio = nombre.strip()
    if not limpio:
        return False
    for p in datos['periodos']:
        if p == limpio:
            return False
    datos['periodos'].append(limpio)
    guardar_datos(datos)
    return True


def obtener_secciones():
    datos = cargar_datos()
    if 'secciones' not in datos:
        datos['secciones'] = ['A', 'B']
        guardar_datos(datos)
    return datos['secciones']


def agregar_seccion(nombre):
    datos = cargar_datos()
    if 'secciones' not in datos:
        datos['secciones'] = []
    if nombre in datos['secciones']:
        return False
    datos['secciones'].append(nombre)
    datos['secciones'].sort()
    guardar_datos(datos)
    return True


def agregar_estudiantes(cedula, nombres, apellidos, year, seccion, periodo='2026-2027'):
    datos = cargar_datos()
    for student in datos['estudiantes']:
        if student['cedula'] == cedula:
            return False
    datos['estudiantes'].append({
        'cedula': cedula,
        'nombres': nombres,
        'apellidos': apellidos,
        'year': year,
        'seccion': seccion,
        'periodo': periodo
    })
    guardar_datos(datos)
    return True


def obtener_est():
    return cargar_datos()['estudiantes']


def eliminar_est(cedula):
    datos = cargar_datos()
    estudiantes_lista = []
    for e in datos['estudiantes']:
        if e['cedula'] != cedula:
            estudiantes_lista.append(e)
    datos['estudiantes'] = estudiantes_lista

    calificaciones_lista = []

    for c in datos['calificaciones']:
        if c['cedula'] != cedula:
            calificaciones_lista.append(c)
    datos['calificaciones'] = calificaciones_lista

    guardar_datos(datos)


def agregar_nota(cedula, materia, lapso, corte, nota, periodo='2026-2027'):
    datos = cargar_datos()
    for calif in datos['calificaciones']:
        per_calif = calif.get('periodo', '2026-2027')
        if (
            calif['cedula'] == cedula
            and calif['materia'] == materia
            and int(calif['lapso']) == int(lapso)
            and int(calif['corte']) == int(corte)
            and per_calif == periodo
        ):
            calif['nota'] = float(nota)
            calif['periodo'] = periodo
            guardar_datos(datos)
            return 'actualizada'

    datos['calificaciones'].append({
        'cedula': cedula,
        'materia': materia,
        'lapso': int(lapso),
        'corte': int(corte),
        'nota': float(nota),
        'periodo': periodo
    })
    guardar_datos(datos)
    return 'creada'


def editar_nota(cedula, materia, lapso, corte, nota_anterior, nueva_nota, periodo=None):
    datos = cargar_datos()
    for calif in datos['calificaciones']:
        per_calif = calif.get('periodo', '2026-2027')
        coincide_periodo = (periodo is None) or (per_calif == periodo)
        if (
            calif['cedula'] == cedula
            and calif['materia'] == materia
            and int(calif['lapso']) == int(lapso)
            and int(calif['corte']) == int(corte)
            and float(calif['nota']) == float(nota_anterior)
            and coincide_periodo
        ):
            calif['nota'] = float(nueva_nota)
            guardar_datos(datos)
            return True
    return False


def notas_estudiantes(cedula, periodo=None):
    datos = cargar_datos()
    resultado = []
    for c in datos['calificaciones']:
        if c['cedula'] == cedula:
            per_calif = c.get('periodo', '2026-2027')
            if periodo is None or periodo == 'Todos' or per_calif == periodo:
                resultado.append(c)
    return resultado


def promedio_materia(cedula, materia, periodo=None):
    notas_lista = notas_estudiantes(cedula, periodo)
    notas = []
    for c in notas_lista:
        if c['materia'] == materia:
            notas.append(float(c['nota']))
    if len(notas) == 0:
        return 0
    return sum(notas) / len(notas)


def obtener_rol(username):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['username'] == username:
            return usuario['rol']
    return None


def obtener_materias():
    datos = cargar_datos()
    if 'materias' not in datos:
        datos['materias'] = []
        guardar_datos(datos)
    return datos['materias']


def agregar_materia(nombre, year):
    datos = cargar_datos()
    if 'materias' not in datos:
        datos['materias'] = []
    for materia in datos['materias']:
        if materia['nombre'] == nombre and materia['year'] == year:
            return False
    datos['materias'].append({'nombre': nombre, 'year': year})
    guardar_datos(datos)
    return True


def eliminar_materia(nombre, year):
    datos = cargar_datos()

    materias_actualizadas = []

    for m in datos['materias']:
        if not (m['nombre'] == nombre and m['year'] == year):
            materias_actualizadas.append(m)
    datos['materias'] = materias_actualizadas

    calificaciones_actualizadas = []
    for c in datos['calificaciones']:
        if not (c['materia'] == nombre and c.get('year', year) == year):
            calificaciones_actualizadas.append(c)
    datos['calificaciones'] = calificaciones_actualizadas

    guardar_datos(datos)

def obtener_nota_aprobatoria():
    datos = cargar_datos()
    config = datos.get('configuracion', {})
    return float(config.get('nota_aprobatoria', 10))


def promedio_estudiante(cedula, periodo=None):
    notas_alumno = notas_estudiantes(cedula, periodo)
    if len(notas_alumno) == 0:
        return 0.0

    suma = 0.0
    for n in notas_alumno:
        suma = suma + float(n['nota'])

    return suma / len(notas_alumno)


def promedio_seccion(year, seccion, periodo=None):
    estudiantes = obtener_est()
    promedio_alumnos = []

    for student in estudiantes:
        if student['year'] == year and student['seccion'] == seccion:
            notas_alumno = notas_estudiantes(student['cedula'], periodo)
            if len(notas_alumno) > 0:
                prom = promedio_estudiante(student['cedula'], periodo)
                promedio_alumnos.append(prom)

    if len(promedio_alumnos) == 0:
        return 0.0

    suma_seccion = 0.0
    for p in promedio_alumnos:
        suma_seccion = suma_seccion + p

    return suma_seccion / len(promedio_alumnos)