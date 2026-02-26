import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from gui.styles import Theme
from gui.windows import WelcomeWindow, ConfigWindow, TestSelectionWindow, ExecutionWindow, ResultsWindow, InstrumentSetupWindow
from engine.config import APP_TITLE, APP_ICON

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.resize(1200, 800)
        
        # Central Widget & Stack
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Initialize Windows
        self.welcome_window = WelcomeWindow(self.navigate_to_config, self.navigate_to_instrument_setup)
        self.config_window = ConfigWindow(self.navigate_to_test_selection, self.navigate_to_welcome, self.handle_config_imported)
        self.test_selection_window = TestSelectionWindow(self.navigate_to_execution, self.navigate_to_config, self.handle_selection_imported)
        self.execution_window = ExecutionWindow(self.navigate_to_results, self.navigate_to_test_selection_from_emergency)
        self.results_window = ResultsWindow(self.navigate_to_welcome)
        self.instrument_setup_window = InstrumentSetupWindow(self.navigate_to_welcome)
        
        self.stack.addWidget(self.welcome_window)          # Index 0
        self.stack.addWidget(self.config_window)           # Index 1
        self.stack.addWidget(self.test_selection_window)   # Index 2
        self.stack.addWidget(self.execution_window)        # Index 3
        self.stack.addWidget(self.results_window)          # Index 4
        self.stack.addWidget(self.instrument_setup_window) # Index 5
        
        self.show()

    def navigate_to_config(self):
        self.stack.setCurrentIndex(1)

    def navigate_to_test_selection(self):
        # Pass configuration data to test selection window for defaults
        data = self.config_window.get_data()
        self.test_selection_window.set_dut_data(data)
        self.stack.setCurrentIndex(2)
        
    def navigate_to_execution(self, selected_tests, test_params, report_format):
        # Get data from config window
        dut_data = self.config_window.get_data()
        self.execution_window.start_execution(selected_tests, dut_data, test_params, report_format)
        self.stack.setCurrentIndex(3)
        
    def navigate_to_results(self, results, dut_data, report_format, logs):
        self.results_window.display_results(results, dut_data, report_format, logs)
        self.stack.setCurrentIndex(4)
        
    def navigate_to_welcome(self):
        self.stack.setCurrentIndex(0)
    
    def navigate_to_instrument_setup(self):
        self.stack.setCurrentIndex(5)
    
    def navigate_to_test_selection_from_emergency(self):
        """Navigate back to test selection after emergency stop"""
        self.stack.setCurrentIndex(2)

    def handle_config_imported(self, session_data):
        """Sync from ConfigWindow to TestSelectionWindow."""
        self.test_selection_window.set_session_data(session_data)

    def handle_selection_imported(self, dut_data):
        """Sync from TestSelectionWindow back to ConfigWindow."""
        self.config_window.set_data(dut_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.get_stylesheet())
    window = MainWindow()
    sys.exit(app.exec())
