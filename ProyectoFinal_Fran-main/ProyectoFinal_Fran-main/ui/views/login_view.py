from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QStackedWidget, QWidget
from database.db import validar_login, registrar_usuario

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Acceso - Sistema Escolar")
        self.resize(340, 280)

        layout_principal = QVBoxLayout()
        self.stack = QStackedWidget()

        self.pagina_login = self.crear_pagina_login()
        self.pagina_registro = self.crear_pagina_registro()

        self.stack.addWidget(self.pagina_login)      
        self.stack.addWidget(self.pagina_registro)   

        layout_principal.addWidget(self.stack)
        self.setLayout(layout_principal)

    def crear_pagina_login(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Iniciar sesión"))

        self.input_login_user = QLineEdit()
        self.input_login_user.setPlaceholderText("Usuario")
        layout.addWidget(self.input_login_user)

        self.input_login_pass = QLineEdit()
        self.input_login_pass.setPlaceholderText("Contraseña")
        self.input_login_pass.setEchoMode(QLineEdit.Password)
        self.input_login_pass.returnPressed.connect(self.verificar_credenciales)
        layout.addWidget(self.input_login_pass)

        btn_entrar = QPushButton("Entrar")
        btn_entrar.clicked.connect(self.verificar_credenciales)
        layout.addWidget(btn_entrar)

        btn_ir_registro = QPushButton("Crear cuenta nueva")
        btn_ir_registro.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_ir_registro)

        widget.setLayout(layout)
        return widget

    def crear_pagina_registro(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Crear cuenta"))

        self.input_reg_user = QLineEdit()
        self.input_reg_user.setPlaceholderText("Elige un usuario")
        layout.addWidget(self.input_reg_user)

        self.combo_reg_rol = QComboBox()
        self.combo_reg_rol.addItems(["Profesor", "Admin"])
        layout.addWidget(self.combo_reg_rol)

        self.input_reg_pass = QLineEdit()
        self.input_reg_pass.setPlaceholderText("Contraseña")
        self.input_reg_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_reg_pass)

        btn_registrar = QPushButton("Registrar usuario")
        btn_registrar.clicked.connect(self.registrar)
        layout.addWidget(btn_registrar)

        btn_volver_login = QPushButton("Ya tengo cuenta — Iniciar sesión")
        btn_volver_login.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_volver_login)

        widget.setLayout(layout)
        return widget

    def verificar_credenciales(self):
        usuario = self.input_login_user.text().strip()
        password = self.input_login_pass.text()

        if validar_login(usuario, password):
            self.usuario_actual = usuario
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos')


    def registrar(self):
        usuario = self.input_reg_user.text().strip()
        password = self.input_reg_pass.text()
        rol = self.combo_reg_rol.currentText()

        if not usuario or not password:
            QMessageBox.warning(self, 'Error', 'Completa todos los campos')
            return
        if registrar_usuario(usuario, password, rol):
            QMessageBox.information(self, 'Éxito', 'Usuario creado. Ya puedes iniciar sesión')
            self.input_reg_user.clear()
            self.input_reg_pass.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, 'Error', 'Ese usuario ya existe')