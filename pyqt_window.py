from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

def create_window():
    window = QMainWindow()
    window.setWindowTitle("Chatbot UI")
    window.resize(800, 600)

    webview = QWebEngineView()
    webview.load(QUrl("http://127.0.0.1:8000/static/universe_ui.html"))

    window.setCentralWidget(webview)
    return window
