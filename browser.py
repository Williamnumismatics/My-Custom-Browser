from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

app = QApplication(sys.argv)

# Main Window
window = QMainWindow()
window.setWindowTitle("Pyra")
window.setGeometry(100, 100, 1200, 800)

# Toolbar
toolbar = QToolBar()
window.addToolBar(toolbar)

# Browser
browser = QWebEngineView()
browser.setUrl(QUrl("https://www.google.com"))
tabs = QTabWidget()
window.setCentralWidget(tabs)
# Address Bar
url_bar = QLineEdit()
toolbar.addWidget(url_bar)

def navigate_to_url():
    text = url_bar.text().strip()
    
    if text.startswith("http://") or text.startswith("https://"):
        url = text
    elif "." in text:  # simple domain check
        url = "http://" + text
    else:  # treat as search query
        query = "+".join(text.split())
        url = f"https://www.google.com/search?q={query}"
    
    browser.setUrl(QUrl(url))

url_bar.returnPressed.connect(navigate_to_url)

# Back / Forward / Reload Buttons
back_btn = QAction("Back", window)
back_btn.triggered.connect(browser.back)
toolbar.addAction(back_btn)

forward_btn = QAction("Forward", window)
forward_btn.triggered.connect(browser.forward)
toolbar.addAction(forward_btn)

reload_btn = QAction("Reload", window)
reload_btn.triggered.connect(browser.reload)
toolbar.addAction(reload_btn)

# Update address bar when URL changes
def update_url_bar(qurl):
    url_bar.setText(qurl.toString())

def create_new_tab(url="https://www.google.com", label="New Tab"):
    new_browser = QWebEngineView()
    new_browser.setUrl(QUrl(url))
    index = tabs.addTab(new_browser, label)
    tabs.setCurrentIndex(index)
    new_browser.urlChanged.connect(lambda q: url_bar.setText(q.toString()))
    new_browser.titleChanged.connect(lambda t: tabs.setTabText(index, t))
    return new_browser

browser.urlChanged.connect(update_url_bar)

window.show()
sys.exit(app.exec_())
