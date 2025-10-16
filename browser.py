from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

# Initialize the app
app = QApplication(sys.argv)

# Create the main window
window = QMainWindow()
window.setWindowTitle("Pyra")
window.setGeometry(100, 100, 1200, 800)

# Create the tab widget
tabs = QTabWidget()
window.setCentralWidget(tabs)

# Toolbar with buttons and address bar
toolbar = QToolBar()
window.addToolBar(toolbar)

url_bar = QLineEdit()
toolbar.addWidget(url_bar)

# Functions to handle tabs
def get_current_browser():
    return tabs.currentWidget()

def create_new_tab(url="https://www.google.com", label="New Tab"):
    browser = QWebEngineView()
    browser.setUrl(QUrl(url))
    index = tabs.addTab(browser, label)
    tabs.setCurrentIndex(index)

    # Update address bar when page changes
    browser.urlChanged.connect(lambda q: url_bar.setText(q.toString()))
    # Update tab title
    browser.titleChanged.connect(lambda t: tabs.setTabText(index, t))

    return browser

# Navigation functions
def navigate_to_url():
    browser = get_current_browser()
    text = url_bar.text().strip()

    if text.startswith("http://") or text.startswith("https://"):
        url = text
    elif "." in text:  # looks like a domain
        url = "http://" + text
    else:  # treat as a search query
        query = "+".join(text.split())
        url = f"https://www.google.com/search?q={query}"

    browser.setUrl(QUrl(url))

# Connect address bar
url_bar.returnPressed.connect(navigate_to_url)

# Back, forward, reload buttons
back_btn = QAction("Back", window)
back_btn.triggered.connect(lambda: get_current_browser().back())
toolbar.addAction(back_btn)

forward_btn = QAction("Forward", window)
forward_btn.triggered.connect(lambda: get_current_browser().forward())
toolbar.addAction(forward_btn)

reload_btn = QAction("Reload", window)
reload_btn.triggered.connect(lambda: get_current_browser().reload())
toolbar.addAction(reload_btn)

# New tab button
new_tab_btn = QAction("New Tab", window)
new_tab_btn.triggered.connect(lambda: create_new_tab())
toolbar.addAction(new_tab_btn)

# Update address bar when switching tabs
def update_url_bar(index):
    browser = tabs.widget(index)
    if browser:
        url_bar.setText(browser.url().toString())

tabs.currentChanged.connect(update_url_bar)

# Create the first tab
create_new_tab()

# Show window
window.show()
sys.exit(app.exec_())
