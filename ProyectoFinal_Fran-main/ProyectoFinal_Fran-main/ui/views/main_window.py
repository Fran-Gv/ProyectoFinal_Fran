from PyQt5.QtWidgets import QMainWindow, QTabWidget
from ui.views.estudiantes_view import EstudiantesView
from ui.views.materias_view import MateriasView
from ui.views.notas_view import NotasView
from ui.views.resumen import ResumenView


class MainWindow(QMainWindow):
    def __init__(self, rol, usuario=''):
        super().__init__()
        if usuario:
            self.setWindowTitle('Sistema Escolar -' + usuario + '('+ str(rol) +')')
        else:
            self.setWindowTitle('Sistema Escolar')
        self.resize(900, 600)


        self.pestanas = QTabWidget()

        self.vista_estudiantes = EstudiantesView(rol)
        self.vista_materias = MateriasView(rol)
        self.vista_notas = NotasView(rol)
        self.vista_resumen = ResumenView(rol)

        self.pestanas.addTab(self.vista_estudiantes, 'Estudiantes')
        self.pestanas.addTab(self.vista_materias, 'Materias')
        self.pestanas.addTab(self.vista_notas, 'Notas')
        self.pestanas.addTab(self.vista_resumen, 'Resumen y Secciones')

        self.pestanas.currentChanged.connect(self.al_cambiar_pestana)

        self.setCentralWidget(self.pestanas)

    def al_cambiar_pestana(self, indice):
        if indice == 0:
            self.vista_estudiantes.cargar_tabla()
        elif indice == 1:
            self.vista_materias.cargar_tabla()
        elif indice == 2:
            self.vista_notas.refrescar()
        elif indice == 3:
            self.vista_resumen.refrescar()
        
        