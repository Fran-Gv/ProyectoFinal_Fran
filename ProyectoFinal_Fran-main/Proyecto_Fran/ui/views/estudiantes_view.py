from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                             QComboBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QHeaderView, QInputDialog)
from database.db import agregar_estudiantes, obtener_est, eliminar_est, obtener_secciones, agregar_seccion

class EstudiantesView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()

        formulario = QFormLayout()

        self.input_cedula = QLineEdit()
        self.input_nombres = QLineEdit()
        self.input_apellidos = QLineEdit()

        self.combo_year = QComboBox()
        self.combo_year.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_seccion = QComboBox()
        self.cargar_secciones()

        formulario.addRow('Cédula:', self.input_cedula)
        formulario.addRow('Nombres:', self.input_nombres)
        formulario.addRow('Apellidos:', self.input_apellidos)
        formulario.addRow('Año:', self.combo_year)
        formulario.addRow('Sección:', self.combo_seccion)

        layout.addLayout(formulario)

        #Botonesヾ(≧▽≦*)o

        but_guardar = QPushButton('Guardar estudiantes')
        but_guardar.clicked.connect(self.guardar)
        layout.addWidget(but_guardar)

        if self.rol == 'Admin':
            but_seccion = QPushButton('Agregar sección')
            but_seccion.clicked.connect(self.nueva_seccion)
            layout.addWidget(but_seccion)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['Cédula', 'Nombres', 'Apellidos', 'Año', 'Sección'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        but_eliminar = QPushButton('Eliminar seleccionado')
        but_eliminar.clicked.connect(self.eliminar)
        layout.addWidget(but_eliminar)

        self.setLayout(layout)
        self.cargar_tabla()

    def guardar(self):
        cedula = self.input_cedula.text().strip()
        nombres = self.input_nombres.text().strip()
        apellidos = self.input_apellidos.text().strip()
        year = self.combo_year.currentText()
        seccion = self.combo_seccion.currentText()

        if not cedula or not nombres or not apellidos:
            QMessageBox.warning(self, 'Error', 'Completa todos los campos')
            return

        if agregar_estudiantes(cedula, nombres, apellidos, year, seccion):
            self.input_cedula.clear()
            self.input_nombres.clear()
            self.input_apellidos.clear()
            self.cargar_tabla()
        else:
            QMessageBox.warning(self, 'Error', 'Ya existe un estudiante con esa cédula')

    def cargar_tabla(self):
        estudiantes = obtener_est()
        self.tabla.setRowCount(len(estudiantes))
        for fila, est in enumerate(estudiantes):
            self.tabla.setItem(fila, 0, QTableWidgetItem(est['cedula']))
            self.tabla.setItem(fila, 1, QTableWidgetItem(est['nombres']))
            self.tabla.setItem(fila, 2, QTableWidgetItem(est['apellidos']))
            self.tabla.setItem(fila, 3, QTableWidgetItem(est['year']))
            self.tabla.setItem(fila, 4, QTableWidgetItem(est['seccion']))
            

    def eliminar(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, 'Error', 'Selecciona un estudiante de la tabla')
            return

        cedula = self.tabla.item(fila, 0).text()
        respuesta = QMessageBox.question(self, 'Confirmar', f'¿Eliminar al estudiante {cedula} y todas sus notas?')

        if respuesta == QMessageBox.Yes:
            eliminar_est(cedula)
            self.cargar_tabla()

    def cargar_secciones(self):
        self.combo_seccion.clear()                     
        self.combo_seccion.addItems(obtener_secciones())

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




    


