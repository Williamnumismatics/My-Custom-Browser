from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
import sys

# ---------- Silent WebEngine Page to suppress JS warnings ----------
class SilentPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass  # ignore all console messages

# ---------- Initialize app ----------
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Pyra")
window.setGeometry(100, 100, 1200, 800)

# ---------- Tabs ----------
tabs = QTabWidget()
tabs.setTabsClosable(True)
tabs.tabCloseRequested.connect(lambda i: tabs.removeTab(i))
window.setCentralWidget(tabs)

# ---------- Toolbar ----------
toolbar = QToolBar()
window.addToolBar(toolbar)

url_bar = QLineEdit()
toolbar.addWidget(url_bar)

# Navigation buttons
back = QAction("Back", window)
forward = QAction("Forward", window)
reload_btn = QAction("Reload", window)
new_tab_btn = QAction("New Tab", window)
bookmark_btn = QAction("Add Bookmark", window)

toolbar.addAction(back)
toolbar.addAction(forward)
toolbar.addAction(reload_btn)
toolbar.addAction(new_tab_btn)
toolbar.addAction(bookmark_btn)

# ---------- Bookmarks Bar ----------
bookmarks_bar_widget = QWidget()
bookmarks_layout = QHBoxLayout()
bookmarks_layout.setContentsMargins(0, 0, 0, 0)
bookmarks_bar_widget.setLayout(bookmarks_layout)
window.addToolBarBreak()
bookmarks_toolbar = QToolBar()
bookmarks_toolbar.addWidget(bookmarks_bar_widget)
window.addToolBar(bookmarks_toolbar)

bookmarks = []

def add_bookmark():
    b = current_browser()
    url = b.url().toString()
    bookmarks.append(url)
    btn = QPushButton(url)
    btn.clicked.connect(lambda _, u=url: go_to_url(u))
    bookmarks_layout.addWidget(btn)

# ---------- Functions ----------
def current_browser():
    return tabs.currentWidget()

def new_tab(url="https://www.google.com", label="New Tab"):
    browser = QWebEngineView()
    page = SilentPage(browser)
    browser.setPage(page)
    browser.setUrl(QUrl(url))
    index = tabs.addTab(browser, label)
    tabs.setCurrentIndex(index)

    browser.urlChanged.connect(lambda q: url_bar.setText(q.toString()))
    browser.titleChanged.connect(lambda t: tabs.setTabText(index, t))
    return browser

def go_to_url(text=None):
    b = current_browser()
    if text is None:
        text = url_bar.text().strip()
    if text.startswith("http://") or text.startswith("https://"):
        url = text
    elif "." in text:
        url = "http://" + text
    else:
        query = "+".join(text.split())
        url = f"https://www.google.com/search?q={query}"
    b.setUrl(QUrl(url))

# ---------- Connect buttons ----------
back.triggered.connect(lambda: current_browser().back())
forward.triggered.connect(lambda: current_browser().forward())
reload_btn.triggered.connect(lambda: current_browser().reload())
new_tab_btn.triggered.connect(lambda: new_tab())
bookmark_btn.triggered.connect(add_bookmark)
url_bar.returnPressed.connect(go_to_url)
tabs.currentChanged.connect(lambda i: url_bar.setText(tabs.widget(i).url().toString()))

# ---------- Open first tab ----------
new_tab()

# ---------- Run ----------
window.show()
sys.exit(app.exec_())
