from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QFileDialog, QHBoxLayout, QMenuBar, QAction
from PyQt5.QtCore import Qt

# MenuBarView class definition
class MenuBarView(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the "File" menu item and its submenu
        file_menu = self.addMenu('File')

        # Add "New", "Export to Excel", and "Quit" to the File menu
        self.new_action = QAction('New', self)
        self.new_action.setDisabled(True)
        file_menu.addAction(self.new_action)

        self.execute_action = QAction('Export to Excel', self)
        self.execute_action.setDisabled(True)
        file_menu.addAction(self.execute_action)

        self.quit_action = QAction('Quit', self)
        self.quit_action.triggered.connect(parent.close)
        file_menu.addAction(self.quit_action)

        # Apply stylesheet to menu items (optional)
        self.setStyleSheet("""
            QMenuBar {
                color: #FFFFFF;
                border-bottom: 1px solid #586075;
                padding: 0px; /* Remove any padding from QMenuBar */
                margin: 0px; /* Remove any margin from QMenuBar */
            }

            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px; /* Adjust this as needed */
                margin: 0px; /* Remove any margin around items */
                font-weight: bold;
            }

            QMenuBar::item:selected { /* When hovered */
                background-color: #586075;
            }

            QMenu {
                background-color: #3E4755;
                color: #FFFFFF;
            }

            QMenu::item:selected { /* When hovered */
                background-color: #586075;
            }

            QMenu::item:disabled { /* For disabled items */
                color: gray;
            }
        """)

def css():
        return """
        """