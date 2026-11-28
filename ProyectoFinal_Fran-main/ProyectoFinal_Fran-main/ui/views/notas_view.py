from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QHBoxLayout, QLabel, QInputDialog
)
from database.db import (
    promedio_seccion, promedio_estudiante, notas_estudiantes,
    obtener_est, obtener_materias, obtener_secciones,
    agregar_nota, editar_nota, obtener_periodos, agregar_periodo
)


class NotasView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()
        form = QFormLayout()

        self.combo_periodo = QComboBox()
        self.combo_periodo.addItems(obtener_periodos())

        self.combo_year = QComboBox()
        self.combo_year.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_seccion = QComboBox()
        self.combo_seccion.addItems(obtener_secciones())

        self.combo_materia = QComboBox()

        self.combo_lapso = QComboBox()
        self.combo_lapso.addItems(['1', '2', '3'])

        self.combo_corte = QComboBox()
        self.combo_corte.addItems(['1', '2', '3'])

        self.combo_estudiantes = QComboBox()

        self.input_notas = QLineEdit()
        self.input_notas.setPlaceholderText('Ej: 16.5')

        form.addRow('Año académico:', self.combo_periodo)
        form.addRow('Año:', self.combo_year)
        form.addRow('Sección:', self.combo_seccion)
        form.addRow('Materia:', self.combo_materia)
        form.addRow('Lapso:', self.combo_lapso)
        form.addRow('Corte:', self.combo_corte)
        form.addRow('Estudiante:', self.combo_estudiantes)
        form.addRow('Nota:', self.input_notas)

        layout.addLayout(form)

        btn_guardar = QPushButton('Guardar nota')
        btn_guardar.clicked.connect(self.guardar_nota)
        layout.addWidget(btn_guardar)

        if self.rol == 'Admin':
            btn_nuevo_periodo = QPushButton('Nuevo año académico')
            btn_nuevo_periodo.clicked.connect(self.nuevo_periodo)
            layout.addWidget(btn_nuevo_periodo)

        fila_filtro_prom = QHBoxLayout()
        self.combo_filtro_lapso = QComboBox()
        self.combo_filtro_lapso.addItems(['Todos', '1', '2', '3'])
        fila_filtro_prom.addWidget(QLabel('Filtrar por lapso:'))
        fila_filtro_prom.addWidget(self.combo_filtro_lapso)
        layout.addLayout(fila_filtro_prom)

        fila_promedios = QHBoxLayout()
        self.prom_estudiante = QLabel('Promedio estudiante: 0')
        self.prom_seccion = QLabel('Promedio sección: 0')
        fila_promedios.addWidget(self.prom_estudiante)
        fila_promedios.addWidget(self.prom_seccion)
        layout.addLayout(fila_promedios)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['Materia', 'Lapso', 'Corte', 'Nota', 'Período'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        btn_editar = QPushButton('Editar nota seleccionada')
        btn_editar.clicked.connect(self.editar_nota_selecionada)
        layout.addWidget(btn_editar)

        self.setLayout(layout)

        self.combo_periodo.currentTextChanged.connect(self.actualizar_vista_alumno)
        self.combo_year.currentTextChanged.connect(self.actualizar_filtros)
        self.combo_seccion.currentTextChanged.connect(self.actualizar_estudiantes)
        self.combo_estudiantes.currentIndexChanged.connect(self.actualizar_vista_alumno)
        self.combo_filtro_lapso.currentTextChanged.connect(self.actualizar_vista_alumno)
        self.actualizar_filtros()

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

    def nuevo_periodo(self):
        texto, ok = QInputDialog.getText(
            self,
            'Nuevo año académico',
            'Escribe el año académico (Ej: 2027-2028):'
        )
        if not ok:
            return
        limpio = texto.strip()
        if not limpio:
            QMessageBox.warning(self, 'Error', 'Escribe un año académico válido')
            return
        if agregar_periodo(limpio):
            self.refrescar()
            self.combo_periodo.setCurrentText(limpio)
            QMessageBox.information(self, 'Listo', 'Año académico ' + limpio + ' creado')
        else:
            QMessageBox.warning(self, 'Error', 'Ese año académico ya existe o no es válido')

    def refrescar(self):
        per_actual = self.combo_periodo.currentText()
        self.combo_periodo.clear()
        self.combo_periodo.addItems(obtener_periodos())
        if per_actual:
            idx_per = self.combo_periodo.findText(per_actual)
            if idx_per >= 0:
                self.combo_periodo.setCurrentIndex(idx_per)

        sec_actual = self.combo_seccion.currentText()
        self.combo_seccion.clear()
        self.combo_seccion.addItems(obtener_secciones())
        if sec_actual:
            indice = self.combo_seccion.findText(sec_actual)
            if indice >= 0:
                self.combo_seccion.setCurrentIndex(indice)
        self.actualizar_filtros()

    def actualizar_vista_alumno(self):
        cedula = self.combo_estudiantes.currentData()
        year = self.combo_year.currentText()
        seccion = self.combo_seccion.currentText()
        periodo = self.combo_periodo.currentText()
        lapso_filtro = self.combo_filtro_lapso.currentText()

        prom_sec_verif = promedio_seccion(year, seccion, periodo)
        if prom_sec_verif is None:
            prom_sec = 0
        else:
            prom_sec = round(prom_sec_verif, 2)
        self.prom_seccion.setText('Promedio sección: ' + str(prom_sec))

        if not cedula:
            self.prom_estudiante.setText('Promedio estudiante: 0')
            self.tabla.setRowCount(0)
            return

        notas_todas = notas_estudiantes(cedula, periodo)
        notas_filtradas = []
        for n in notas_todas:
            if lapso_filtro == 'Todos' or int(n['lapso']) == int(lapso_filtro):
                notas_filtradas.append(n)

        notas_ordenadas = self.ordenar_notas(notas_filtradas)

        if len(notas_ordenadas) == 0:
            prom_est = 0
        elif lapso_filtro == 'Todos':
            prom_est_verif = promedio_estudiante(cedula, periodo)
            if prom_est_verif is None:
                prom_est = 0
            else:
                prom_est = round(prom_est_verif, 2)
        else:
            suma = 0.0
            for n in notas_ordenadas:
                suma = suma + float(n['nota'])
            prom_est = round(suma / len(notas_ordenadas), 2)

        self.prom_estudiante.setText('Promedio estudiante: ' + str(prom_est))

        self.tabla.setRowCount(len(notas_ordenadas))
        for fila, item in enumerate(notas_ordenadas):
            per_item = item.get('periodo', '2026-2027')
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(item['materia'])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(item['lapso'])))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(item['corte'])))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(item['nota'])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(per_item)))

    def actualizar_estudiantes(self):
        year = self.combo_year.currentText()
        seccion = self.combo_seccion.currentText()

        self.combo_estudiantes.clear()
        estudiantes = obtener_est()
        for est in estudiantes:
            if est['year'] == year and est['seccion'] == seccion:
                texto = est['cedula'] + ' - ' + est['apellidos'] + ', ' + est['nombres']
                self.combo_estudiantes.addItem(texto, est['cedula'])

        self.actualizar_vista_alumno()

    def actualizar_filtros(self):
        year = self.combo_year.currentText()

        self.combo_materia.clear()
        materias = obtener_materias()
        for mat in materias:
            if mat['year'] == year:
                self.combo_materia.addItem(mat['nombre'])
        self.actualizar_estudiantes()

    def guardar_nota(self):
        cedula = self.combo_estudiantes.currentData()
        if not cedula:
            QMessageBox.warning(self, 'Error', 'Selecciona un estudiante válido')
            return

        materia = self.combo_materia.currentText()
        if not materia:
            QMessageBox.warning(self, 'Error', 'No hay materias registradas para este año')
            return

        texto_nota = self.input_notas.text().strip().replace(',', '.')
        try:
            nota = float(texto_nota)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Escribe una nota numérica válida')
            return

        if nota < 0 or nota > 20:
            QMessageBox.warning(self, 'Error', 'La nota debe estar entre 0 y 20')
            return

        lapso = int(self.combo_lapso.currentText())
        corte = int(self.combo_corte.currentText())
        periodo = self.combo_periodo.currentText()

        agregar_nota(cedula, materia, lapso, corte, nota, periodo)
        self.input_notas.clear()
        self.actualizar_vista_alumno()
        QMessageBox.information(self, 'Listo', 'Nota guardada correctamente')

    def editar_nota_selecionada(self):
        cedula = self.combo_estudiantes.currentData()
        if not cedula:
            QMessageBox.warning(self, 'Error', 'Selecciona un estudiante válido')
            return

        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, 'Error', 'Selecciona una nota de la tabla para editar')
            return

        materia = self.tabla.item(fila, 0).text()
        lapso = int(self.tabla.item(fila, 1).text())
        corte = int(self.tabla.item(fila, 2).text())
        nota_anterior = float(self.tabla.item(fila, 3).text())
        periodo_fila = self.tabla.item(fila, 4).text()

        nuevo_texto, ok = QInputDialog.getText(
            self,
            'Editar nota',
            'Nueva nota para ' + materia + ' (' + periodo_fila + ', Lapso ' + str(lapso) + ', Corte ' + str(corte) + '):',
            text=str(nota_anterior)
        )
        if not ok:
            return

        nuevo_texto = nuevo_texto.strip().replace(',', '.')
        try:
            nueva_nota = float(nuevo_texto)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Escribe una nota numérica válida')
            return

        if nueva_nota < 0 or nueva_nota > 20:
            QMessageBox.warning(self, 'Error', 'La nota debe estar entre 0 y 20')
            return

        if editar_nota(cedula, materia, lapso, corte, nota_anterior, nueva_nota, periodo_fila):
            self.actualizar_vista_alumno()
            QMessageBox.information(self, 'Listo', 'Nota editada correctamente')
        else:
            QMessageBox.warning(self, 'Error', 'No se pudo actualizar la nota')