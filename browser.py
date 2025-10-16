from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

app = QApplication(sys.argv)
toolbar = QToolBar()

#Main Window
window = QMainWindow()
window.setWindowTitle("Pyra")
window.setGeometry(100,100,1200,800)
window.addToolBar(toolbar)

#Main Tab
browser = QWebEngineView()
browser.setUrl(QUrl("https://www.google.com"))
window.setCentralWidget(browser)


#Back Button
back_btn = QAction("Back", window)
back_btn.triggered.connect(browser.back)
toolbar.addAction(back_btn)

window.show()
sys.exit(app.exec_())