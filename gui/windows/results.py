from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QMessageBox, QFileDialog)
from reports.generator import ReportGenerator
from engine.config import REPORTS_OUTPUT_DIR
import datetime
import os

class ResultsWindow(QWidget):
    def __init__(self, on_home_callback):
        super().__init__()
        layout = QVBoxLayout(self)
        
        header = QLabel("Test Results Confirmation")
        header.setObjectName("HeaderLabel")
        layout.addWidget(header)
        
        # Result List
        self.result_table = QListWidget()
        layout.addWidget(self.result_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        home = QPushButton("Start New Test")
        home.clicked.connect(on_home_callback)
        
        self.report_btn = QPushButton("Generate Report")
        self.report_btn.setObjectName("PrimaryButton")
        self.report_btn.clicked.connect(self.generate_report)
        
        btn_layout.addWidget(home)
        btn_layout.addStretch()
        btn_layout.addWidget(self.report_btn)
        layout.addLayout(btn_layout)
        
        self.latest_data = None
        self.dut_data = None
        self.report_fmt = "PDF"

    def display_results(self, results, dut_data, report_fmt, logs=""):
        self.latest_data = results
        self.dut_data = dut_data
        self.report_fmt = report_fmt
        self.execution_logs = logs
        
        self.result_table.clear()
        for res in results:
            item_text = f"{res['name']} ... {res['status']}"
            self.result_table.addItem(item_text)
            
    def generate_report(self):
        if not self.dut_data:
             QMessageBox.warning(self, "Data Missing", "No DUT data available. Cannot generate report.")
             return

        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"TestReport_{timestamp}"
            
            # Determine file filter and extension based on format
            if self.report_fmt == "Word":
                file_filter = "Word Documents (*.docx)"
                default_filename += ".docx"
            else:
                file_filter = "PDF Files (*.pdf)"
                default_filename += ".pdf"

            # 1. Ask user where to save (defaults to reports/output/)
            os.makedirs(REPORTS_OUTPUT_DIR, exist_ok=True)
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report As",
                os.path.join(REPORTS_OUTPUT_DIR, default_filename),
                file_filter
            )

            # 2. Check if user cancelled
            if not file_path:
                return

            # Extract images from results
            all_images = []
            for res in self.latest_data:
                if "images" in res:
                    all_images.extend(res["images"])
                 
            gen = ReportGenerator(
                file_path, 
                self.dut_data, 
                self.latest_data, 
                self.dut_data.get("Tester Name", "Admin"),
                logs=self.execution_logs,
                images=all_images
            )
            
            if self.report_fmt == "PDF":
                gen.generate_pdf()
            else:
                gen.generate_word()
                
            QMessageBox.information(self, "Report Generated", f"Saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Report Error", f"Failed to generate report:\n{str(e)}")
