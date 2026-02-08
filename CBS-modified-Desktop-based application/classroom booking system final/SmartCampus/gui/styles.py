"""
Bold & Modern Stylesheet for PyQt5 Application
"""

MODERN_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #0F172A, stop:1 #1E293B);
    }
    
    QWidget {
        background-color: #1E293B;
        color: #F1F5F9;
    }
    
    QLabel {
        color: #F1F5F9;
        font-size: 11px;
    }
    
    QLineEdit {
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 12px;
        background-color: #0F172A;
        color: #F1F5F9;
        font-size: 11px;
        selection-background-color: #06B6D4;
    }
    
    QLineEdit:focus {
        border: 2px solid #06B6D4;
        background-color: #1E293B;
    }
    
    QLineEdit:hover {
        border: 2px solid #0EA5E9;
    }
    
    QTextEdit {
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 12px;
        background-color: #0F172A;
        color: #F1F5F9;
        font-size: 11px;
        selection-background-color: #06B6D4;
    }
    
    QTextEdit:focus {
        border: 2px solid #06B6D4;
        background-color: #1E293B;
    }
    
    QComboBox {
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 12px;
        background-color: #0F172A;
        color: #F1F5F9;
        font-size: 11px;
    }
    
    QComboBox:focus {
        border: 2px solid #06B6D4;
        background-color: #1E293B;
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
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 12px;
        background-color: #0F172A;
        color: #F1F5F9;
        font-size: 11px;
    }
    
    QDateEdit:focus, QTimeEdit:focus {
        border: 2px solid #06B6D4;
        background-color: #1E293B;
    }
    
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #06B6D4, stop:1 #0891B2);
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #0EA5E9, stop:1 #06B6D4);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #0284C7, stop:1 #0E7490);
    }
    
    QPushButton:disabled {
        background-color: #334155;
        color: #64748B;
    }
    
    QPushButton#DangerButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #EF4444, stop:1 #DC2626);
    }
    
    QPushButton#DangerButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #F87171, stop:1 #EF4444);
    }
    
    QPushButton#SuccessButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #10B981, stop:1 #059669);
    }
    
    QPushButton#SuccessButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #34D399, stop:1 #10B981);
    }
    
    QPushButton#WarningButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #F59E0B, stop:1 #D97706);
    }
    
    QPushButton#WarningButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #FBBF24, stop:1 #F59E0B);
    }
    
    QTableWidget {
        border: 2px solid #334155;
        background-color: #0F172A;
        alternate-background-color: #1E293B;
        gridline-color: #334155;
    }
    
    QTableWidget::item {
        padding: 8px;
        color: #F1F5F9;
    }
    
    QTableWidget::item:selected {
        background-color: #0891B2;
        color: #FFFFFF;
    }
    
    QHeaderView::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #06B6D4, stop:1 #0891B2);
        color: #FFFFFF;
        padding: 10px;
        border: none;
        border-right: 1px solid #0E7490;
        font-weight: bold;
        font-size: 11px;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #1E293B;
        width: 14px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:vertical {
        background: #475569;
        border-radius: 7px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #06B6D4;
    }
    
    QScrollBar:horizontal {
        border: none;
        background: #1E293B;
        height: 14px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:horizontal {
        background: #475569;
        border-radius: 7px;
        min-width: 30px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background: #06B6D4;
    }
    
    QTabWidget::pane {
        border: 2px solid #334155;
        background-color: #1E293B;
    }
    
    QTabBar::tab {
        background-color: #0F172A;
        border: 2px solid #334155;
        padding: 12px 18px;
        color: #E2E8F0;
        font-weight: bold;
        font-size: 12px;
        min-width: 130px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #06B6D4, stop:1 #0891B2);
        color: #FFFFFF;
        border-bottom: 3px solid #06B6D4;
        font-size: 12px;
    }
    
    QTabBar::tab:hover {
        background-color: #334155;
        color: #E2E8F0;
    }
    
    QMenuBar {
        background-color: #0F172A;
        color: #F1F5F9;
        border-bottom: 2px solid #06B6D4;
    }
    
    QMenuBar::item:selected {
        background-color: #06B6D4;
        color: #FFFFFF;
    }
    
    QMenu {
        background-color: #1E293B;
        color: #F1F5F9;
        border: 2px solid #334155;
    }
    
    QMenu::item:selected {
        background-color: #06B6D4;
        color: #FFFFFF;
    }
    
    QStatusBar {
        background-color: #0F172A;
        color: #94A3B8;
        border-top: 2px solid #334155;
    }
    
    QCheckBox {
        color: #F1F5F9;
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
    }
    
    QCheckBox::indicator:unchecked {
        background-color: #0F172A;
        border: 2px solid #334155;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #06B6D4;
        border: 2px solid #06B6D4;
        border-radius: 4px;
    }
    
    QRadioButton {
        color: #F1F5F9;
        spacing: 8px;
    }
    
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
    }
    
    QRadioButton::indicator:unchecked {
        background-color: #0F172A;
        border: 2px solid #334155;
        border-radius: 10px;
    }
    
    QRadioButton::indicator:checked {
        background-color: #06B6D4;
        border: 2px solid #06B6D4;
        border-radius: 10px;
    }
    
    QGroupBox {
        border: 2px solid #334155;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 12px;
        color: #F1F5F9;
        font-weight: bold;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 5px 0 5px;
    }
    
    QMessageBox QLabel {
        color: #F1F5F9;
    }
    
    QMessageBox {
        background-color: #1E293B;
    }
    
    QSplitter::handle {
        background-color: #334155;
    }
    
    QToolTip {
        background-color: #0F172A;
        color: #FFFFFF;
        border: 2px solid #06B6D4;
        border-radius: 6px;
        padding: 6px 10px;
    }
"""

TITLE_STYLE = """
    color: #06B6D4;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 16px;
"""

SUBTITLE_STYLE = """
    color: #E2E8F0;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 12px;
"""

CARD_STYLE = """
    QFrame {
        background-color: #1E293B;
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 20px;
    }
"""

SUCCESS_LABEL_STYLE = """
    color: #10B981;
    font-weight: bold;
"""

ERROR_LABEL_STYLE = """
    color: #EF4444;
    font-weight: bold;
"""

WARNING_LABEL_STYLE = """
    color: #F59E0B;
    font-weight: bold;
"""

INFO_LABEL_STYLE = """
    color: #06B6D4;
    font-weight: bold;
"""
