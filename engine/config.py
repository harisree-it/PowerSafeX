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
TEMPLATE_DIR = os.path.join(REPORTS_DIR, "template")       # source template (tracked in git)
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, REPORT_TEMPLATE_NAME)
REPORTS_OUTPUT_DIR = os.path.join(REPORTS_DIR, "output")   # generated .docx/.pdf reports
CAPTURES_DIR = os.path.join(REPORTS_DIR, "captures")       # scope screenshots

# User data
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUPS_DIR = os.path.join(DATA_DIR, "backups")            # "Backup Settings" JSON exports
