import os

# Report Generation Settings
REPORT_PASSWORD = "admin"
REPORT_TEMPLATE_NAME = "Test report demo.docx"

# Theme / UI Constants (can be expanded)
APP_TITLE = "PowerSafe - Converter Test Automation"
APP_ICON = "assets/icon.png"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TEMPLATE_PATH = os.path.join(REPORTS_DIR, REPORT_TEMPLATE_NAME)
