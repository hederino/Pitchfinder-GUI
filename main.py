import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from widgets import Widget, MainWindowSubwidget, ExitButton, FreqWindow
from note import Note
from settings import settings, save_settings

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pitchfinder GUI")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setFixedSize(400, 220)
        self.init_UI()
        self.set_menubar()
        self.connect_signals()
        self.load_settings()

    def init_UI(self):    
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(Widget())
        self.main_subwidget = MainWindowSubwidget()
        self.main_layout.addWidget(self.main_subwidget)
        self.exit_button_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.exit_button_layout)
        self.exit_button = ExitButton()
        self.exit_button_layout.addSpacing(self.width() - 2 * self.exit_button.width())
        self.exit_button_layout.addWidget(self.exit_button)
        self.centralWidget().setLayout(self.main_layout)
        self.freq_window = FreqWindow()

    def set_menubar(self):
        self.menubar = QtWidgets.QMenuBar()
        settings_menu = self.menubar.addMenu("&Settings")
        help = self.menubar.addMenu("&Help")
        self.about_qt = QtGui.QAction("About Qt...", help)
        help.addAction(self.about_qt)
        
        self.adjust_a4 = settings_menu.addAction("")
        self.set_adjust_a4_txt = lambda: self.adjust_a4.setText(
            f"Set reference frequency of {Note.note_a4()} ...")
        self.set_adjust_a4_txt()

        note_display = settings_menu.addMenu("Note names")
        abc = QtGui.QAction("A, B, C", note_display)
        note_display.addAction(abc)
        self.do_re_mi = QtGui.QAction("Do, Re, Mi", note_display)
        note_display.addAction(self.do_re_mi)
        note_display_group = QtGui.QActionGroup(note_display)
        note_display_group.addAction(abc)
        note_display_group.addAction(self.do_re_mi)
        note_display_group.setExclusive(True)
        abc.setCheckable(True)
        abc.setChecked(True)
        self.do_re_mi.setCheckable(True)
        self.setMenuBar(self.menubar)

    def connect_signals(self):
        self.line_edit = self.main_subwidget.line_edit_widget.line_edit
        self.display_label = self.main_subwidget.display_label
        self.enter_button = self.main_subwidget.line_edit_widget.enter_button 

        def display_label_set_text():
            txt = self.display_label.lineedit_to_label_text(self.line_edit.text())
            self.display_label.setText(txt)

        self.enter_button.clicked.connect(display_label_set_text)
        self.line_edit.returnPressed.connect(self.enter_button.click)
        self.exit_button.clicked.connect(self.close)
        self.freq_window.freq_changed.connect(Note.set_a4)
        self.freq_window.freq_changed.connect(self.enter_button.click)
        self.freq_window.ok_button.clicked.connect(self.freq_window.emit_signal_and_close)
        self.about_qt.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(self, "About Qt"))
        self.adjust_a4.triggered.connect(self.freq_window.show)
        self.do_re_mi.toggled.connect(self.update_upon_note_name_change)
        self.freq_window.reset_button.clicked.connect(self.freq_window.reset_freq)
        self.freq_window.cancel_button.clicked.connect(self.freq_window.close)

    @QtCore.pyqtSlot()
    def update_upon_note_name_change(self):
        Note.switch_note_display()
        self.freq_window.update_upon_note_name_change()
        self.enter_button.click()  # activate button to update text
        self.set_adjust_a4_txt()

    def load_settings(self):
        Note.set_a4(settings["a4"])
        self.do_re_mi.setChecked(settings["do_re_mi_toggled"])

    def closeEvent(self, ev):
        save_settings(Note.freq_a4, self.do_re_mi.isChecked())


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()  
