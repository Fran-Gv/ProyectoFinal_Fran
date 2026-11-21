from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                             QComboBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QHeaderView, QInputDialog)
from database.db import promedio_seccion, promedio_estudiante, promedio_materia, notas_estudiantes, obtener_est, obtener_materias, obtener_secciones

class NotasView(QWidget):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol

        layout = QVBoxLayout()
        form = QFormLayout()

        self.combo_year = QComboBox()
        self.combo_year.addItems(['1er año', '2do año', '3er año', '4to año', '5to año'])

        self.combo_seccion = QComboBox()
        self.combo_seccion.addItems(obtener_secciones())

        self.combo_lapso = QComboBox()
        self.combo_lapso.addItems(['1er', '2do', '3er'])

        self.combo_corte = QComboBox()
        self.combo_corte.addItems(['1er', '2do', '3er'])

        self.combo_estudiantes = QComboBox()

        self.input_notas = QLineEdit()
        self.input_notas.setPlaceholderText('Ej: 16.5')

        form.addRow('Año', self.combo_year)
        form.addRow('Sección', self.combo_seccion)
        form.addRow('Lapso', self.combo_lapso)
        form.addRow('Corte', self.combo_corte)
        form.addRow('Estudiante', self.combo_estudiante)
        form.addRow('Notas', self.input_notas)


        
        
        
        
        
        




