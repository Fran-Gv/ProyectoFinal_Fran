from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.setWindowTitle("Inicio de Sesión - Sistema Escolar")
        self.resize(300, 250)
        
        # Layout principal (Organiza las cosas de arriba hacia abajo)
        layout = QVBoxLayout()
        
        # Título de la ventana
        titulo = QLabel("Bienvenido al Sistema")
        # Un poco de estilo provisional mientras hacemos el QSS
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;") 
        layout.addWidget(titulo)
        
        # Campo de Usuario
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nombre de Usuario")
        layout.addWidget(self.input_usuario)
        
        # Campo de Contraseña
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password) # Oculta la clave con puntitos
        layout.addWidget(self.input_password)
        
        # Botón para Iniciar Sesión
        self.btn_login = QPushButton("Iniciar Sesión")
        # Aquí conectamos el click del botón con la función de abajo
        self.btn_login.clicked.connect(self.verificar_credenciales)
        layout.addWidget(self.btn_login)
        
        # Aplicamos el diseño a la ventana
        self.setLayout(layout)

    # Función temporal para probar el botón
    def verificar_credenciales(self):
        usuario = self.input_usuario.text()
        password = self.input_password.text()
        
        # Credenciales de prueba
        if usuario == "admin" and password == "1234":
            QMessageBox.information(self, "Éxito", "¡Inicio de sesión correcto!")
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")