from PyQt5.QtWidgets import QMainWindow, QTabWidget
from ui.views.estudiantes_view import EstudiantesView
from ui.views.materias_view import MateriasView

class MainWindow(QMainWindow):
    def __init__(self, rol):
        super().__init__()
        self.setWindowTitle('Sistema Escolar')
        self.resize(900, 600)

        pestanas = QTabWidget()
        pestanas.addTab(EstudiantesView(rol), 'Estudiantes')
        pestanas.addTab(MateriasView(rol), 'Materias')

        self.setCentralWidget(pestanas)
        
        