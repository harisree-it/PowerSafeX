from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QHBoxLayout, QMessageBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFileInfo, QTimer
import os


class BlockEditorWindow(QMainWindow):
    def __init__(self, test_name, test_params=None, existing_xml=None, on_save_callback=None):
        super().__init__()
        self.setWindowTitle(f"Block Editor - {test_name}")
        self.resize(1000, 800)
        
        self.test_name = test_name
        self.test_params = test_params or {}
        self.on_save = on_save_callback
        print(f"BlockEditor initialized with XML: {str(existing_xml)[:50]}...")
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Web View
        self.webview = QWebEngineView()
        
        layout.addWidget(self.webview)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Sequence")
        save_btn.clicked.connect(self.save_sequence)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        # Wait for load to finish to inject XML
        if existing_xml:
            self.pending_xml = existing_xml
            # Delay injection to ensure JS is fully ready
            self.webview.loadFinished.connect(lambda: QTimer.singleShot(500, self.inject_xml_and_params))
        else:
            self.pending_xml = None
            # Even if no XML, we need to inject params
            self.webview.loadFinished.connect(lambda: QTimer.singleShot(500, self.inject_params_only))

        # Load local HTML (AFTER connecting signals)
        editor_path = os.path.abspath("assets/blockly/editor.html")
        self.webview.setUrl(QUrl.fromLocalFile(editor_path))

        # Connect console messages
        self.webview.page().javaScriptConsoleMessage = self.log_console_message

    def log_console_message(self, level, message, line, source):
        print(f"JS Console: {message} (Line {line}, Source: {source})")

    def inject_params_only(self):
        # Inject params
        import json
        param_keys = list(self.test_params.keys())
        print(f"Injecting Params: {param_keys}")
        js_params = json.dumps(param_keys)
        self.webview.page().runJavaScript(f"setAvailableParams({js_params});")

    def inject_xml_and_params(self):
        # First inject params so blocks can be rendered correctly? 
        # Actually blocks render fine even if params update later, but better to do it.
        self.inject_params_only()
        
        if self.pending_xml:
            print(f"Injecting XML: {self.pending_xml[:50]}...") # Debug print
            # Escape newlines and quotes for JS string
            safe_xml = self.pending_xml.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
            js = f"setXML('{safe_xml}');"
            self.webview.page().runJavaScript(js)
            self.pending_xml = None
        else:
            print("No pending XML to inject.")

    def save_sequence(self):
        # 1. Get Python Code
        self.webview.page().runJavaScript("getPythonCode()", self.handle_python_code)
        
    def handle_python_code(self, python_code):
        self.generated_code = python_code
        # 2. Get XML
        self.webview.page().runJavaScript("getXML()", self.handle_xml)
        
    def handle_xml(self, xml_text):
        self.xml_content = xml_text
        
        # Now save both
        if self.on_save:
            self.on_save(self.test_name, self.generated_code, self.xml_content)
            
        QMessageBox.information(self, "Saved", "Sequence saved successfully.")
        self.close()
