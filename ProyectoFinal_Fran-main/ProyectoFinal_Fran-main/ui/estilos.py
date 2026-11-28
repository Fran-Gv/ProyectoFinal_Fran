from PyQt5.QtWidgets import QApplication


def cargar_estilos(app):
    if not isinstance(app, QApplication):
        return

    qss = """
    QWidget {
        background-color: #0f172a;
        color: #e2e8f0;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 13px;
    }

    QDialog {
        background-color: #0f172a;
        color: #e2e8f0;
    }

    QTabWidget::pane {
        border: 1px solid #1e293b;
        border-radius: 8px;
        background-color: #111827;
        padding: 6px;
    }

    QTabBar::tab {
        background-color: #1e293b;
        color: #94a3b8;
        padding: 8px 16px;
        margin-right: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        font-weight: bold;
    }

    QTabBar::tab:selected {
        background-color: #0284c7;
        color: #ffffff;
    }

    QTabBar::tab:hover:!selected {
        background-color: #334155;
        color: #f8fafc;
    }

    QLabel {
        color: #f1f5f9;
        background-color: transparent;
    }

    QLineEdit, QComboBox {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 6px 10px;
        selection-background-color: #38bdf8;
        selection-color: #0f172a;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #38bdf8;
    }

    QComboBox::drop-down {
        border: none;
        width: 24px;
    }

    QComboBox QAbstractItemView {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #38bdf8;
        selection-background-color: #0284c7;
        selection-color: #ffffff;
    }

    QPushButton {
        background-color: #0284c7;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #38bdf8;
        color: #0f172a;
    }

    QPushButton:pressed {
        background-color: #0369a1;
        color: #ffffff;
    }

    QTableWidget {
        background-color: #1e293b;
        alternate-background-color: #172033;
        color: #f1f5f9;
        gridline-color: #334155;
        border: 1px solid #334155;
        border-radius: 6px;
    }

    QTableWidget::item:selected {
        background-color: #0284c7;
        color: #ffffff;
    }

    QHeaderView::section {
        background-color: #0f172a;
        color: #38bdf8;
        padding: 6px;
        border: 1px solid #334155;
        font-weight: bold;
    }

    QMessageBox {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    """
    app.setStyleSheet(qss)