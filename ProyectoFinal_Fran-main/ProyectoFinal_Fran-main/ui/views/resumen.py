from PyQt5.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)
from database.db import (
    notas_estudiantes, obtener_est, obtener_secciones, obtener_materias,
    promedio_seccion, obtener_nota_aprobatoria, obtener_periodos
)


class ResumenView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()

   
        layout.addWidget(QLabel('Resumen por estudiante'))
        form_est = QFormLayout()

        self.combo_year_est = QComboBox()
        self.combo_year_est.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_sec_est = QComboBox()
        self.combo_sec_est.addItems(obtener_secciones())

        self.combo_alumno = QComboBox()

        self.combo_periodo_res = QComboBox()
        self.combo_periodo_res.addItem('Todos')
        self.combo_periodo_res.addItems(obtener_periodos())

        self.combo_lapso_res = QComboBox()
        self.combo_lapso_res.addItems(['Todos', '1', '2', '3'])

        self.combo_materia_res = QComboBox()

        form_est.addRow('Año:', self.combo_year_est)
        form_est.addRow('Sección:', self.combo_sec_est)
        form_est.addRow('Estudiante:', self.combo_alumno)
        form_est.addRow('Año académico:', self.combo_periodo_res)
        form_est.addRow('Lapso:', self.combo_lapso_res)
        form_est.addRow('Materia:', self.combo_materia_res)
        layout.addLayout(form_est)

        self.lbl_prom_materia = QLabel('Promedio en materia: 0')
        layout.addWidget(self.lbl_prom_materia)

        fila_cortes = QHBoxLayout()
        self.lbl_corte_1 = QLabel('1er corte: 0')
        self.lbl_corte_2 = QLabel('2do corte: 0')
        self.lbl_corte_3 = QLabel('3er corte: 0')
        fila_cortes.addWidget(self.lbl_corte_1)
        fila_cortes.addWidget(self.lbl_corte_2)
        fila_cortes.addWidget(self.lbl_corte_3)
        layout.addLayout(fila_cortes)

        fila_lapsos = QHBoxLayout()
        self.lbl_lapso_1 = QLabel('1er lapso: 0')
        self.lbl_lapso_2 = QLabel('2do lapso: 0')
        self.lbl_lapso_3 = QLabel('3er lapso: 0')
        fila_lapsos.addWidget(self.lbl_lapso_1)
        fila_lapsos.addWidget(self.lbl_lapso_2)
        fila_lapsos.addWidget(self.lbl_lapso_3)
        layout.addLayout(fila_lapsos)

        self.lbl_promedio_alumno = QLabel('Promedio general (suma de lapsos): 0')
        layout.addWidget(self.lbl_promedio_alumno)

        self.lbl_estado_alumno = QLabel('Estado: Sin notas')
        layout.addWidget(self.lbl_estado_alumno)

        self.tabla_notas = QTableWidget()
        self.tabla_notas.setColumnCount(5)
        self.tabla_notas.setHorizontalHeaderLabels(['Materia', 'Lapso', 'Corte', 'Nota', 'Período'])
        self.tabla_notas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_notas.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla_notas)


        layout.addWidget(QLabel('Comparativa de promedios por sección'))
        fila_sec = QHBoxLayout()

        self.combo_year_sec = QComboBox()
        self.combo_year_sec.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_periodo_sec = QComboBox()
        self.combo_periodo_sec.addItem('Todos')
        self.combo_periodo_sec.addItems(obtener_periodos())

        btn_comparar = QPushButton('Calcular promedios de sección')
        btn_comparar.clicked.connect(self.actualizar_secciones)

        fila_sec.addWidget(QLabel('Año:'))
        fila_sec.addWidget(self.combo_year_sec)
        fila_sec.addWidget(QLabel('Período:'))
        fila_sec.addWidget(self.combo_periodo_sec)
        fila_sec.addWidget(btn_comparar)
        layout.addLayout(fila_sec)

        self.lbl_mejor_seccion = QLabel('Sección con mayor promedio: Sin notas registradas')
        layout.addWidget(self.lbl_mejor_seccion)

        self.tabla_secciones = QTableWidget()
        self.tabla_secciones.setColumnCount(2)
        self.tabla_secciones.setHorizontalHeaderLabels(['Sección', 'Promedio'])
        self.tabla_secciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_secciones.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla_secciones)

        self.setLayout(layout)

        self.combo_year_est.currentTextChanged.connect(self.cargar_materias_filtro)
        self.combo_year_est.currentTextChanged.connect(self.cargar_alumnos)
        self.combo_sec_est.currentTextChanged.connect(self.cargar_alumnos)
        self.combo_alumno.currentIndexChanged.connect(self.mostrar_detalle_alumno)
        self.combo_periodo_res.currentTextChanged.connect(self.mostrar_detalle_alumno)
        self.combo_lapso_res.currentTextChanged.connect(self.mostrar_detalle_alumno)
        self.combo_materia_res.currentTextChanged.connect(self.mostrar_detalle_alumno)
        self.combo_year_sec.currentTextChanged.connect(self.actualizar_secciones)
        self.combo_periodo_sec.currentTextChanged.connect(self.actualizar_secciones)

        self.refrescar()

    def ordenar_notas(self, lista_notas):
        ordenadas = list(lista_notas)
        for i in range(len(ordenadas)):
            for j in range(i + 1, len(ordenadas)):
                lap_i = int(ordenadas[i]['lapso'])
                lap_j = int(ordenadas[j]['lapso'])
                cor_i = int(ordenadas[i]['corte'])
                cor_j = int(ordenadas[j]['corte'])
                mat_i = str(ordenadas[i]['materia']).lower()
                mat_j = str(ordenadas[j]['materia']).lower()

                debe_intercambiar = False
                if lap_j < lap_i:
                    debe_intercambiar = True
                elif lap_j == lap_i and cor_j < cor_i:
                    debe_intercambiar = True
                elif lap_j == lap_i and cor_j == cor_i and mat_j < mat_i:
                    debe_intercambiar = True

                if debe_intercambiar:
                    aux = ordenadas[i]
                    ordenadas[i] = ordenadas[j]
                    ordenadas[j] = aux
        return ordenadas

    def filtrar_notas(self, lista_notas, lapso=None, corte=None, materia=None):
        resultado = []
        for item in lista_notas:
            if lapso is not None and lapso != 'Todos':
                if int(item['lapso']) != int(lapso):
                    continue
            if corte is not None:
                if int(item['corte']) != int(corte):
                    continue
            if materia is not None and materia != '' and materia != 'Todas':
                if str(item['materia']) != materia:
                    continue
            resultado.append(item)
        return resultado

    def calcular_promedio_lista(self, lista_notas):
        if len(lista_notas) == 0:
            return 0.0
        suma = 0.0
        for item in lista_notas:
            suma = suma + float(item['nota'])
        return round(suma / len(lista_notas), 2)

    def refrescar(self):
        per_res_actual = self.combo_periodo_res.currentText()
        self.combo_periodo_res.clear()
        self.combo_periodo_res.addItem('Todos')
        self.combo_periodo_res.addItems(obtener_periodos())
        if per_res_actual:
            idx = self.combo_periodo_res.findText(per_res_actual)
            if idx >= 0:
                self.combo_periodo_res.setCurrentIndex(idx)

        per_sec_actual = self.combo_periodo_sec.currentText()
        self.combo_periodo_sec.clear()
        self.combo_periodo_sec.addItem('Todos')
        self.combo_periodo_sec.addItems(obtener_periodos())
        if per_sec_actual:
            idx_sec = self.combo_periodo_sec.findText(per_sec_actual)
            if idx_sec >= 0:
                self.combo_periodo_sec.setCurrentIndex(idx_sec)

        sec_actual = self.combo_sec_est.currentText()
        self.combo_sec_est.clear()
        self.combo_sec_est.addItems(obtener_secciones())
        if sec_actual:
            indice = self.combo_sec_est.findText(sec_actual)
            if indice >= 0:
                self.combo_sec_est.setCurrentIndex(indice)

        self.cargar_materias_filtro()
        self.cargar_alumnos()
        self.actualizar_secciones()

    def cargar_materias_filtro(self):
        year = self.combo_year_est.currentText()
        materia_anterior = self.combo_materia_res.currentText()

        self.combo_materia_res.clear()
        self.combo_materia_res.addItem('Todas')

        materias = obtener_materias()
        for mat in materias:
            if str(mat['year']) == year:
                self.combo_materia_res.addItem(str(mat['nombre']))

        if materia_anterior:
            idx = self.combo_materia_res.findText(materia_anterior)
            if idx >= 0:
                self.combo_materia_res.setCurrentIndex(idx)

    def cargar_alumnos(self):
        year = self.combo_year_est.currentText()
        seccion = self.combo_sec_est.currentText()
        cedula_anterior = self.combo_alumno.currentData()

        self.combo_alumno.clear()
        estudiantes = obtener_est()
        for est in estudiantes:
            if est['year'] == year and est['seccion'] == seccion:
                texto = est['cedula'] + ' - ' + est['apellidos'] + ', ' + est['nombres']
                self.combo_alumno.addItem(texto, est['cedula'])

        if cedula_anterior:
            for i in range(self.combo_alumno.count()):
                if self.combo_alumno.itemData(i) == cedula_anterior:
                    self.combo_alumno.setCurrentIndex(i)
                    break

        self.mostrar_detalle_alumno()

    def mostrar_detalle_alumno(self):
        cedula = self.combo_alumno.currentData()
        periodo = self.combo_periodo_res.currentText()
        lapso = self.combo_lapso_res.currentText()
        materia_sel = self.combo_materia_res.currentText()

        if not cedula:
            self.lbl_prom_materia.setText('Promedio en materia: 0')
            self.lbl_corte_1.setText('1er corte: 0')
            self.lbl_corte_2.setText('2do corte: 0')
            self.lbl_corte_3.setText('3er corte: 0')
            self.lbl_lapso_1.setText('1er lapso: 0')
            self.lbl_lapso_2.setText('2do lapso: 0')
            self.lbl_lapso_3.setText('3er lapso: 0')
            self.lbl_promedio_alumno.setText('Promedio general (suma de lapsos): 0')
            self.lbl_estado_alumno.setText('Estado: Sin notas')
            self.tabla_notas.setRowCount(0)
            return

        notas_periodo = notas_estudiantes(cedula, periodo)

        prom_l1 = self.calcular_promedio_lista(self.filtrar_notas(notas_periodo, lapso=1))
        prom_l2 = self.calcular_promedio_lista(self.filtrar_notas(notas_periodo, lapso=2))
        prom_l3 = self.calcular_promedio_lista(self.filtrar_notas(notas_periodo, lapso=3))

        self.lbl_lapso_1.setText('1er lapso: ' + str(prom_l1))
        self.lbl_lapso_2.setText('2do lapso: ' + str(prom_l2))
        self.lbl_lapso_3.setText('3er lapso: ' + str(prom_l3))

        promedios_lapsos = []
        for p in [prom_l1, prom_l2, prom_l3]:
            if p > 0:
                promedios_lapsos.append(p)

        if len(promedios_lapsos) == 0:
            prom_general = 0
        else:
            suma_lapsos = 0.0
            for p in promedios_lapsos:
                suma_lapsos = suma_lapsos + float(p)
            prom_general = round(suma_lapsos / len(promedios_lapsos), 2)

        self.lbl_promedio_alumno.setText('Promedio general (suma de lapsos): ' + str(prom_general))

        notas_lapso = self.filtrar_notas(notas_periodo, lapso=lapso)

        self.lbl_corte_1.setText('1er corte: ' + str(self.calcular_promedio_lista(self.filtrar_notas(notas_lapso, corte=1))))
        self.lbl_corte_2.setText('2do corte: ' + str(self.calcular_promedio_lista(self.filtrar_notas(notas_lapso, corte=2))))
        self.lbl_corte_3.setText('3er corte: ' + str(self.calcular_promedio_lista(self.filtrar_notas(notas_lapso, corte=3))))

        if materia_sel == 'Todas' or materia_sel == '':
            self.lbl_prom_materia.setText('Promedio en materia: Selecciona una materia')
        else:
            prom_mat = self.calcular_promedio_lista(self.filtrar_notas(notas_lapso, materia=materia_sel))
            self.lbl_prom_materia.setText('Promedio en ' + materia_sel + ': ' + str(prom_mat))

        notas_ordenadas = self.ordenar_notas(self.filtrar_notas(notas_lapso, materia=materia_sel))

        if len(notas_periodo) == 0:
            self.lbl_estado_alumno.setText('Estado: Sin notas')
        else:
            nota_minima = obtener_nota_aprobatoria()
            if prom_general >= nota_minima:
                self.lbl_estado_alumno.setText('Estado: Aprobado')
            else:
                self.lbl_estado_alumno.setText('Estado: Reprobado')

        self.tabla_notas.setRowCount(len(notas_ordenadas))
        for fila, item in enumerate(notas_ordenadas):
            per_item = item.get('periodo', '2026-2027')
            self.tabla_notas.setItem(fila, 0, QTableWidgetItem(str(item['materia'])))
            self.tabla_notas.setItem(fila, 1, QTableWidgetItem(str(item['lapso'])))
            self.tabla_notas.setItem(fila, 2, QTableWidgetItem(str(item['corte'])))
            self.tabla_notas.setItem(fila, 3, QTableWidgetItem(str(item['nota'])))
            self.tabla_notas.setItem(fila, 4, QTableWidgetItem(str(per_item)))

    def actualizar_secciones(self):
        year = self.combo_year_sec.currentText()
        periodo = self.combo_periodo_sec.currentText()
        secciones = obtener_secciones()

        self.tabla_secciones.setRowCount(len(secciones))
        mejor_sec = None
        mejor_prom = -1.0

        for fila, sec in enumerate(secciones):
            prom_verif = promedio_seccion(year, sec, periodo)

            if prom_verif is None:
                prom = 0
            else:
                prom = round(prom_verif, 2)
            self.tabla_secciones.setItem(fila, 0, QTableWidgetItem(str(sec)))
            self.tabla_secciones.setItem(fila, 1, QTableWidgetItem(str(prom)))

            if prom > mejor_prom:
                mejor_prom = prom
                mejor_sec = sec

        if mejor_sec is not None and mejor_prom > 0:
            self.lbl_mejor_seccion.setText(
                'Sección con mayor promedio en ' + year + ' (' + periodo + '): ' + str(mejor_sec) + ' (' + str(mejor_prom) + ')'
            )
        else:
            self.lbl_mejor_seccion.setText('Sección con mayor promedio: Sin notas registradas')