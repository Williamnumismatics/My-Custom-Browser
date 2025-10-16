from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Pyra")
window.setGeometry(100,100,1200,800)

browser = QWebEngineView()
browser.setUrl("https://www.google.com")
window.setCentralWidget(browser)

window.show()
sys.exit(app.exec_())