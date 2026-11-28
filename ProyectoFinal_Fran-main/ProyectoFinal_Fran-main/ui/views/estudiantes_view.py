from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,  QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QPushButton, QTableWidget, QLabel,
    QTableWidgetItem, QMessageBox, QHeaderView, QInputDialog
)
from database.db import (
    agregar_estudiantes, obtener_est, eliminar_est,
    obtener_secciones, agregar_seccion, obtener_periodos, agregar_periodo
)

class EstudiantesView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()
        formulario = QFormLayout()

        self.combo_periodo = QComboBox()

        self.input_cedula = QLineEdit()
        self.input_nombres = QLineEdit()
        self.input_apellidos = QLineEdit()

        self.combo_year = QComboBox()
        self.combo_year.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_seccion = QComboBox()
        self.cargar_secciones()

        formulario.addRow('Año académico:', self.combo_periodo)
        formulario.addRow('Cédula:', self.input_cedula)
        formulario.addRow('Nombres:', self.input_nombres)
        formulario.addRow('Apellidos:', self.input_apellidos)
        formulario.addRow('Año:', self.combo_year)
        formulario.addRow('Sección:', self.combo_seccion)

        layout.addLayout(formulario)

        but_guardar = QPushButton('Guardar estudiantes')
        but_guardar.clicked.connect(self.guardar)
        layout.addWidget(but_guardar)

        if self.rol == 'Admin':
            but_periodo = QPushButton('Nuevo año académico')
            but_periodo.clicked.connect(self.nuevo_periodo)
            layout.addWidget(but_periodo)

            but_seccion = QPushButton('Agregar sección')
            but_seccion.clicked.connect(self.nueva_seccion)
            layout.addWidget(but_seccion)

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText('Buscar por cédula, nombre o apellido...')
        layout.addWidget(self.input_buscar)

        filtros_layout = QHBoxLayout()

        self.filtro_year = QComboBox()
        self.filtro_year.addItems(['Todos', '1er año', '2do año', '3er año', '4to año', '5to año'])

        self.filtro_periodo = QComboBox()
        self.cargar_periodos()

        filtros_layout.addWidget(QLabel('Filtrar año'))
        filtros_layout.addWidget(self.filtro_year)
        filtros_layout.addWidget(QLabel('Filtrar período'))
        filtros_layout.addWidget(self.filtro_periodo)
        layout.addLayout(filtros_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(['Cédula', 'Nombres', 'Apellidos', 'Año', 'Sección', 'Período'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        if self.rol == 'Admin':
            but_eliminar = QPushButton('Eliminar seleccionado')
            but_eliminar.clicked.connect(self.eliminar)
            layout.addWidget(but_eliminar)

        # Conectar señales una vez que todos los widgets existen
        self.input_buscar.textChanged.connect(self.cargar_tabla)
        self.filtro_year.currentTextChanged.connect(self.cargar_tabla)
        self.filtro_periodo.currentTextChanged.connect(self.cargar_tabla)

        self.setLayout(layout)
        self.cargar_tabla()

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
            self.cargar_periodos()
            self.combo_periodo.setCurrentText(limpio)
            QMessageBox.information(self, 'Listo', 'Año académico ' + limpio + ' creado')
        else:
            QMessageBox.warning(self, 'Error', 'Ese año académico ya existe o no es válido')

    def guardar(self):
        cedula = self.input_cedula.text().strip()
        nombres = self.input_nombres.text().strip().title()
        apellidos = self.input_apellidos.text().strip().title()
        year = self.combo_year.currentText()
        seccion = self.combo_seccion.currentText()
        periodo = self.combo_periodo.currentText()

        if not cedula or not nombres or not apellidos:
            QMessageBox.warning(self, 'Error', 'Completa todos los campos')
            return

        if agregar_estudiantes(cedula, nombres, apellidos, year, seccion, periodo):
            self.input_cedula.clear()
            self.input_nombres.clear()
            self.input_apellidos.clear()
            self.cargar_tabla()
        else:
            QMessageBox.warning(self, 'Error', 'Ya existe un estudiante con esa cédula')

    def cargar_tabla(self):
        if not hasattr(self, 'tabla'):
            return

        texto_busqueda = self.input_buscar.text().strip().lower()
        year_filtro = self.filtro_year.currentText()
        periodo_filtro = self.filtro_periodo.currentText()
        estudiantes = obtener_est()

        ordenados = list(estudiantes)
        for i in range(len(ordenados)):
            for j in range(i + 1, len(ordenados)):
                clave_i = ordenados[i]['apellidos'].lower() + ' ' + ordenados[i]['nombres'].lower()
                clave_j = ordenados[j]['apellidos'].lower() + ' ' + ordenados[j]['nombres'].lower()
                if clave_j < clave_i:
                    aux = ordenados[i]
                    ordenados[i] = ordenados[j]
                    ordenados[j] = aux

        filtrados = []
        for est in ordenados:
            if year_filtro != 'Todos':
                if str(est['year']) != year_filtro:
                    continue

            per_est = est.get('periodo', '2026-2027')
            if periodo_filtro != 'Todos':
                if str(per_est) != periodo_filtro:
                    continue

            if texto_busqueda != '':
                coincide_cedula = texto_busqueda in str(est['cedula']).lower()
                coincide_nombre = texto_busqueda in str(est['nombres']).lower()
                coincide_apellido = texto_busqueda in str(est['apellidos']).lower()
                if not coincide_cedula and not coincide_nombre and not coincide_apellido:
                    continue

            filtrados.append(est)

        self.tabla.setRowCount(len(filtrados))
        for fila in range(len(filtrados)):
            est = filtrados[fila]
            per_est = est.get('periodo', '2026-2027')
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(est['cedula'])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(est['nombres'])))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(est['apellidos'])))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(est['year'])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(est['seccion'])))
            self.tabla.setItem(fila, 5, QTableWidgetItem(str(per_est)))

    def eliminar(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, 'Error', 'Selecciona un estudiante de la tabla')
            return

        cedula = self.tabla.item(fila, 0).text()
        respuesta = QMessageBox.question(
            self,
            'Confirmar',
            '¿Eliminar al estudiante ' + cedula + ' y todas sus notas?'
        )

        if respuesta == QMessageBox.Yes:
            eliminar_est(cedula)
            self.cargar_tabla()

    def cargar_secciones(self):
        self.combo_seccion.clear()
        self.combo_seccion.addItems(obtener_secciones())

    def cargar_periodos(self):
        actual = self.combo_periodo.currentText()
        actual_filtro = self.filtro_periodo.currentText()
        periodos = obtener_periodos()

        self.combo_periodo.clear()
        for p in periodos:
            self.combo_periodo.addItem(p)

        if actual != '':
            indice = self.combo_periodo.findText(actual)
            if indice >= 0:
                self.combo_periodo.setCurrentIndex(indice)

        self.filtro_periodo.clear()
        self.filtro_periodo.addItem('Todos')
        for p in periodos:
            self.filtro_periodo.addItem(p)

        if actual_filtro != '':
            indice_filtro = self.filtro_periodo.findText(actual_filtro)
            if indice_filtro >= 0:
                self.filtro_periodo.setCurrentIndex(indice_filtro)

    def nueva_seccion(self):
        texto, ok = QInputDialog.getText(self, 'Nueva sección', 'Nombre de la sección')
        if not ok:
            return
        texto = texto.strip().upper()
        if not texto:
            QMessageBox.warning(self, 'Error', 'Escribe un nombre')
            return
        if agregar_seccion(texto):
            self.cargar_secciones()
            self.combo_seccion.setCurrentText(texto)
        else:
            QMessageBox.warning(self, 'Error', 'Esa sección ya existe')