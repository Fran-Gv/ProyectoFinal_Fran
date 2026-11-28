from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QHeaderView, QHBoxLayout, QLabel)
from database.db import obtener_materias, agregar_materia, eliminar_materia

class MateriasView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()
       
        if self.rol == 'Admin':
            form = QFormLayout()
            self.input_nombre = QLineEdit()
            self.combo_year = QComboBox()
            self.combo_year.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

            form.addRow('Materia:', self.input_nombre)
            form.addRow('Año:', self.combo_year)
            layout.addLayout(form)

            but_guardar = QPushButton('Guardar')
            but_guardar.clicked.connect(self.guardar)
            layout.addWidget(but_guardar)
        
        filtro_layout = QHBoxLayout()
        self.filtro_year = QComboBox()
        self.filtro_year.addItems(['Todos', '1er año', '2do año', '3er año', '4to año', '5to año'])
        filtro_layout.addWidget(QLabel('Filtrar por año:'))
        filtro_layout.addWidget(self.filtro_year)
        layout.addLayout(filtro_layout)
 
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(['Materias', 'Años'])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        self.filtro_year.currentTextChanged.connect(self.cargar_tabla)

        if self.rol == 'Admin':
            but_eliminar = QPushButton('Eliminar seleccionada')
            but_eliminar.clicked.connect(self.eliminar)
            layout.addWidget(but_eliminar)

        self.setLayout(layout)
        self.cargar_tabla()

    def guardar(self):
        nombre = self.input_nombre.text().strip().title()
        year = self.combo_year.currentText()

        if not nombre:
            QMessageBox.warning(self, 'Error', 'Escribe el nombre de la materia')
            return

        if agregar_materia(nombre, year):
            self.input_nombre.clear()
            self.cargar_tabla()
        else:
            QMessageBox.warning(self, 'Error', 'Esa materia ya existe en ese año')

    def cargar_tabla(self):
        year_filtro = self.filtro_year.currentText()
        materias = obtener_materias()

        filtradas = []
        for mat in materias:
            if year_filtro != 'Todos':
                if str(mat['year']) != year_filtro:
                    continue
            filtradas.append(mat)

        self.tabla.setRowCount(len(filtradas))
        for fila in range(len(filtradas)):
            mat = filtradas[fila]
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(mat['nombre'])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(mat['year'])))

    def eliminar(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, 'Error', 'Selecciona una materia de la tabla')
            return

        nombre = self.tabla.item(fila, 0).text()
        year = self.tabla.item(fila, 1).text()
        respuesta = QMessageBox.question(self, 'Confirmar', f'¿Eliminar {nombre} de {year}?')

        if respuesta == QMessageBox.Yes:
            eliminar_materia(nombre, year)
            self.cargar_tabla()

        
    


            



    
