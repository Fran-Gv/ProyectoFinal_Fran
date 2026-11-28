import sys
from PyQt5.QtWidgets import QApplication
from database.db import crear_admin, obtener_rol
from ui.estilos import cargar_estilos
from ui.views.login_view import LoginWindow
from ui.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    cargar_estilos(app)

    crear_admin()

    login = LoginWindow()
    if login.exec_() == LoginWindow.Accepted:
        usuario = getattr(login, 'usuario_actual', '')
        rol = obtener_rol(usuario)
        if rol is None:
            rol = 'Profesor'

        ventana = MainWindow(rol, usuario)
        ventana.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()