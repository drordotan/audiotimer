from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog

class MenuBarController:

    def __init__(self, controller):
        self.controller = controller
        self.view = None
        self.model = None

    def set_vm(self, view, model):
        self.view = view
        self.model = model

    def new(self):
        # Remove existing widgets from the layout or central widget
        if self.view.workView in self.view.main_layout.children():
            self.view.main_layout.removeWidget(self.view.workView)
            self.view.workView.deleteLater()  # Mark for deletion

        if self.view.soundView.scroll_area in self.view.main_layout.children():
            self.view.main_layout.removeWidget(self.view.soundView.scroll_area)
            self.view.soundView.scroll_area.deleteLater()  # Mark for deletion

        if self.view.tableView in self.view.main_layout.children():
            self.view.main_layout.removeWidget(self.view.tableView)
            self.view.tableView.deleteLater()  # Mark for deletion

        # Disable menu items
        self.view.menuBarView.new_action.setEnabled(False)
        self.view.menuBarView.new_action.setProperty("class", "menu_item_disabled")
        self.view.menuBarView.execute_action.setEnabled(False)
        self.view.menuBarView.execute_action.setProperty("class", "menu_item_disabled")

        # Reset files through the controller
        self.controller.openWorkController.reset_files()

        # Reset labels
        self.view.audio_button.setText("Select Audio")
        self.view.xlsx_button.setText("Select Xlsx")

        # Update the layout after modifications
        self.view.main_layout.update()  # Refresh the layout
        # Or you can also use self.view.main_layout.adjustSize() if necessary


    def on_new(self):
        # Enable menu items and set appropriate names/styles
        self.view.menuBarView.new_action.setEnabled(True)
        self.view.menuBarView.new_action.setProperty("class", "file_menu_item")
        self.view.menuBarView.new_action.triggered.connect(self.new)

        self.view.menuBarView.execute_action.setEnabled(True)
        self.view.menuBarView.execute_action.setProperty("class", "file_menu_item")
        self.view.menuBarView.execute_action.triggered.connect(self.save_to_excel)

    def save_to_excel(self):
        # Open a file dialog to select the save path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("xlsx")

        selected_file_path, _ = file_dialog.getSaveFileName(
            parent=None,
            caption="Save File",
            directory="",
            filter="Excel Files (*.xlsx)",
            options=options
        )

        if selected_file_path:
            # Save to the specified path
            self.model.exportModel.save_to_xlsx(
                self.controller.tableController.get_entries(),
                f"{selected_file_path}.xlsx"
            )
