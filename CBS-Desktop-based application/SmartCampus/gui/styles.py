"""
Modern Stylesheet for PyQt5 Application
"""

MODERN_STYLESHEET = """
    QMainWindow {
        background-color: #F3F4F6;
    }
    
    QWidget {
        background-color: #FFFFFF;
        color: #1F2937;
    }
    
    QLabel {
        color: #1F2937;
        font-size: 10px;
    }
    
    QLineEdit {
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        padding: 8px;
        background-color: #FFFFFF;
        color: #1F2937;
        font-size: 10px;
        selection-background-color: #2563EB;
    }
    
    QLineEdit:focus {
        border: 2px solid #2563EB;
    }
    
    QLineEdit:hover {
        border: 1px solid #2563EB;
    }
    
    QTextEdit {
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        padding: 8px;
        background-color: #FFFFFF;
        color: #1F2937;
        font-size: 10px;
        selection-background-color: #2563EB;
    }
    
    QTextEdit:focus {
        border: 2px solid #2563EB;
    }
    
    QComboBox {
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        padding: 8px;
        background-color: #FFFFFF;
        color: #1F2937;
        font-size: 10px;
    }
    
    QComboBox:focus {
        border: 2px solid #2563EB;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        width: 12px;
        height: 12px;
    }
    
    QDateEdit, QTimeEdit {
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        padding: 8px;
        background-color: #FFFFFF;
        color: #1F2937;
        font-size: 10px;
    }
    
    QDateEdit:focus, QTimeEdit:focus {
        border: 2px solid #2563EB;
    }
    
    QPushButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 10px;
    }
    
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    
    QPushButton:pressed {
        background-color: #1E40AF;
    }
    
    QPushButton:disabled {
        background-color: #D1D5DB;
        color: #9CA3AF;
    }
    
    QPushButton#DangerButton {
        background-color: #DC2626;
    }
    
    QPushButton#DangerButton:hover {
        background-color: #B91C1C;
    }
    
    QPushButton#SuccessButton {
        background-color: #059669;
    }
    
    QPushButton#SuccessButton:hover {
        background-color: #047857;
    }
    
    QPushButton#WarningButton {
        background-color: #F59E0B;
    }
    
    QPushButton#WarningButton:hover {
        background-color: #D97706;
    }
    
    QTableWidget {
        border: 1px solid #E5E7EB;
        background-color: #FFFFFF;
        alternate-background-color: #F9FAFB;
        gridline-color: #E5E7EB;
    }
    
    QTableWidget::item {
        padding: 5px;
        color: #1F2937;
    }
    
    QTableWidget::item:selected {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    
    QHeaderView::section {
        background-color: #2563EB;
        color: #FFFFFF;
        padding: 5px;
        border: none;
        border-right: 1px solid #1E40AF;
        font-weight: bold;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #F3F4F6;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background: #CBD5E1;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #94A3B8;
    }
    
    QScrollBar:horizontal {
        border: none;
        background: #F3F4F6;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background: #CBD5E1;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background: #94A3B8;
    }
    
    QTabWidget::pane {
        border: 1px solid #E5E7EB;
    }
    
    QTabBar::tab {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        padding: 8px 16px;
        color: #6B7280;
    }
    
    QTabBar::tab:selected {
        background-color: #FFFFFF;
        color: #2563EB;
        border-bottom: 2px solid #2563EB;
    }
    
    QTabBar::tab:hover {
        background-color: #FFFFFF;
    }
    
    QMenuBar {
        background-color: #FFFFFF;
        color: #1F2937;
        border-bottom: 1px solid #E5E7EB;
    }
    
    QMenuBar::item:selected {
        background-color: #2563EB;
        color: #FFFFFF;
    }
    
    QMenu {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #E5E7EB;
    }
    
    QMenu::item:selected {
        background-color: #DBEAFE;
        color: #2563EB;
    }
    
    QStatusBar {
        background-color: #FFFFFF;
        color: #6B7280;
        border-top: 1px solid #E5E7EB;
    }
    
    QCheckBox {
        color: #1F2937;
        spacing: 5px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    
    QCheckBox::indicator:unchecked {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 3px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #2563EB;
        border: 1px solid #2563EB;
        border-radius: 3px;
    }
    
    QRadioButton {
        color: #1F2937;
        spacing: 5px;
    }
    
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
    }
    
    QRadioButton::indicator:unchecked {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 9px;
    }
    
    QRadioButton::indicator:checked {
        background-color: #2563EB;
        border: 1px solid #2563EB;
        border-radius: 9px;
    }
    
    QGroupBox {
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
        color: #1F2937;
        font-weight: bold;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
    
    QMessageBox QLabel {
        color: #1F2937;
    }
    
    QMessageBox {
        background-color: #FFFFFF;
    }
    
    QSplitter::handle {
        background-color: #E5E7EB;
    }
    
    QToolTip {
        background-color: #1F2937;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
    }
"""

TITLE_STYLE = """
    color: #2563EB;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 16px;
"""

SUBTITLE_STYLE = """
    color: #374151;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 12px;
"""

CARD_STYLE = """
    QFrame {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
    }
"""

SUCCESS_LABEL_STYLE = """
    color: #059669;
    font-weight: bold;
"""

ERROR_LABEL_STYLE = """
    color: #DC2626;
    font-weight: bold;
"""

WARNING_LABEL_STYLE = """
    color: #F59E0B;
    font-weight: bold;
"""

INFO_LABEL_STYLE = """
    color: #0EA5E9;
    font-weight: bold;
"""
