from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from gui.styles import Theme

class WelcomeWindow(QWidget):
    def __init__(self, on_start_callback, on_setup_callback=None):
        super().__init__()
        self.on_setup_callback = on_setup_callback
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(100)
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_pixmap = QPixmap("assets/welcome_logo.png")
        if not logo_pixmap.isNull():
             # Scale if too large, e.g. max 400px height or width
             if logo_pixmap.width() > 600:
                 logo_pixmap = logo_pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
             logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label)
        layout.addSpacing(100)

        title = QLabel("PowerSafe Test Automation")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        layout.addSpacing(300)
        
        # Instrument Setup Button
        setup_btn = QPushButton("⚙️ Instrument Setup")
        setup_btn.setFixedSize(200, 50)
        if hasattr(self, 'on_setup_callback') and self.on_setup_callback:
            setup_btn.clicked.connect(self.on_setup_callback)
        layout.addWidget(setup_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(10)
        
        start_btn = QPushButton("Start Test")
        start_btn.setObjectName("PrimaryButton")
        start_btn.setFixedSize(200, 50)
        start_btn.clicked.connect(on_start_callback)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        footer = QLabel("Design and Developed by DIN R&D TPS Team for Internal Validation of Converters")
        footer.setStyleSheet(f"color: {Theme.BORDER};")
        layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignCenter)
