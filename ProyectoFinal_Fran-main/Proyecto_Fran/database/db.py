import os
import json
import hashlib

ruta_json = os.path.join(os.path.dirname(__file__), 'datos.json')

datos_inicio = {
    'configuracion': {
        'nombre_colegio': 'Colegio',
        'escala_maxima': 20,
        'nota_aprobatoria' :10
    },
    'usuarios': [],
    'estudiantes': [],
    'secciones': ['A', 'B'],
    'materias': [],
    'calificaciones': [],
    'reparaciones' : []
}




def cargar_datos():
    if not os.path.exists(ruta_json):
        guardar_datos(datos_inicio)
        return json.loads(json.dumps(datos_inicio))
    with open(ruta_json, 'r', encoding= 'utf-8') as archivo:
        return json.load(archivo)

def guardar_datos(datos):
    with open(ruta_json, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def encriptar(password):
    return hashlib.sha256(password.encode()).hexdigest()

def crear_admin():
    datos = cargar_datos()
    if len(datos['usuarios']) == 0:
        datos['usuarios'].append({
            'username' : 'admin',
            'password_hash' : encriptar('1234'),
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
        'password_hash' : encriptar(password),
        'rol' : rol
       })

    guardar_datos(datos)
    return True

def validar_login(username, password):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['username'] == username and usuario['password_hash'] == encriptar(password):
            return True
    return False

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
    

def agregar_estudiantes(cedula, nombres, apellidos, year, seccion):
    datos = cargar_datos()
    for student in datos['estudiantes']:
        if student['cedula'] == cedula:
            return False
    datos['estudiantes'].append({
        'cedula': cedula,
        'nombres': nombres,
        'apellidos': apellidos,
        'year': year,
        'seccion' : seccion
    })

    guardar_datos(datos)
    return True

def obtener_est():
    return cargar_datos()['estudiantes']

def eliminar_est(cedula):
    datos = cargar_datos()
    datos['estudiantes'] = [e for e in datos['estudiantes'] if e['cedula'] != cedula]
    datos['calificaciones'] = [c for c in datos['calificaciones'] if c['cedula'] != cedula]
    guardar_datos(datos)

def agregar_nota(cedula, materia, lapso, corte, nota):
    datos =  cargar_datos()
    datos['calificaciones'].append({
        'cedula': cedula,
        'materia': materia,
        'lapso': lapso,
        'corte': corte,
        'nota': nota
    })
    guardar_datos(datos)

def notas_estudiantes(cedula):
    datos = cargar_datos()
    return [c for c in datos['calificaciones'] if c['cedula'] == cedula]

def promedio_materia(cedula, materia):
    notas = [c['nota'] for c in notas_estudiantes(cedula) if c['materia'] == materia]
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
    datos['materias'] = [m for m in datos['materias']
                         if not (m['nombre'] == nombre and m['year'] == year)]
    guardar_datos(datos)




    