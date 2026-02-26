
class Theme:
    # Colors (Dracula/Catppuccin inspired for modern dark look)
    BACKGROUND = "#1E1E2E"
    FOREGROUND = "#CDD6F4"
    
    PRIMARY = "#89B4FA"      # Blue
    SECONDARY = "#45475A"    # Surface 1
    ACCENT = "#F38BA8"       # Red/Pink (for errors or stops)
    SUCCESS = "#A6E3A1"      # Green
    WARNING = "#F9E2AF"      # Yellow
    
    SURFACE = "#313244"      # Slightly lighter background
    BORDER = "#585B70"
    
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_MAIN = "14px"
    FONT_SIZE_HEADER = "18px"
    FONT_SIZE_TITLE = "24px"

    @staticmethod
    def get_stylesheet():
        return f"""
        QMainWindow {{
            background-color: {Theme.BACKGROUND};
        }}
        QWidget {{
            background-color: {Theme.BACKGROUND};
            color: {Theme.FOREGROUND};
            font-family: "{Theme.FONT_FAMILY}";
            font-size: {Theme.FONT_SIZE_MAIN};
        }}
        /* Labels */
        QLabel {{
            color: {Theme.FOREGROUND};
        }}
        QLabel#HeaderLabel {{
            font-size: {Theme.FONT_SIZE_HEADER};
            font-weight: bold;
            color: {Theme.PRIMARY};
        }}
        QLabel#TitleLabel {{
            font-size: {Theme.FONT_SIZE_TITLE};
            font-weight: bold;
            color: {Theme.PRIMARY};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {Theme.SECONDARY};
            color: {Theme.FOREGROUND};
            border: 1px solid {Theme.BORDER};
            border-radius: 8px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{
            background-color: {Theme.SURFACE};
            border: 1px solid {Theme.PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Theme.PRIMARY};
            color: {Theme.BACKGROUND};
        }}
        QPushButton#PrimaryButton {{
            background-color: {Theme.PRIMARY};
            color: {Theme.BACKGROUND};
            font-weight: bold;
        }}
        QPushButton#PrimaryButton:hover {{
            background-color: #B4BEFE;
        }}
        QPushButton#EmergencyStop {{
            background-color: {Theme.ACCENT};
            color: {Theme.BACKGROUND};
            font-weight: bold;
            font-size: 16px;
            border-radius: 12px;
        }}
        QPushButton#EmergencyStop:hover {{
            background-color: #FF0000;
        }}

        /* Inputs */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background-color: {Theme.SURFACE};
            border: 1px solid {Theme.BORDER};
            border-radius: 4px;
            padding: 4px;
            color: {Theme.FOREGROUND};
            selection-background-color: {Theme.PRIMARY};
        }}
        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {Theme.PRIMARY};
        }}
        
        /* GroupBox */
        QGroupBox {{
            border: 1px solid {Theme.BORDER};
            border-radius: 8px;
            margin-top: 20px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            color: {Theme.PRIMARY};
        }}

        /* ProgressBar */
        QProgressBar {{
            border: 1px solid {Theme.BORDER};
            border-radius: 4px;
            text-align: center;
            background-color: {Theme.SURFACE};
        }}
        QProgressBar::chunk {{
            background-color: {Theme.PRIMARY};
            border-radius: 4px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {Theme.SURFACE};
            border: 1px solid {Theme.BORDER};
            border-radius: 4px;
        }}
        QListWidget::item {{
            padding: 5px;
        }}
        QListWidget::item:selected {{
            background-color: {Theme.PRIMARY};
            color: {Theme.BACKGROUND};
        }}
        """
