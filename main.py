import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from widgets import Widget, MainWindowSubwidget, ExitButton, FreqWindow
from note import Note

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pitchfinder GUI")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setFixedSize(400, 220)
        self.init_UI()
        self.set_menubar()
        self.connect_signals()

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

    def set_menubar(self):
        self.menubar = QtWidgets.QMenuBar()
        settings_menu = self.menubar.addMenu("&Settings")
        help = self.menubar.addMenu("&Help")
        about_qt = QtGui.QAction("About Qt...", help)
        help.addAction(about_qt)
        about_qt.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(self, "About Qt"))
        adjust_a4 = settings_menu.addAction("Set reference frequency of A4...")

        self.freq_window = FreqWindow()

        note_display = settings_menu.addMenu("Note names")

        abc = QtGui.QAction("A, B, C", note_display)
        note_display.addAction(abc)

        do_re_mi = QtGui.QAction("Do, Re, Mi", note_display)
        note_display.addAction(do_re_mi)

        note_display_group = QtGui.QActionGroup(note_display)
        note_display_group.addAction(abc)
        note_display_group.addAction(do_re_mi)
        note_display_group.setExclusive(True)

        abc.setCheckable(True)
        abc.setChecked(True)
        do_re_mi.setCheckable(True)

        do_re_mi.toggled.connect(Note.switch_note_display)
        adjust_a4.triggered.connect(self.freq_window.show)
        # connect to update texts containing note representations
        self.setMenuBar(self.menubar)

    def connect_signals(self):
        line_edit = self.main_subwidget.line_edit_widget.line_edit
        display_label = self.main_subwidget.display_label
        enter_button = self.main_subwidget.line_edit_widget.input_button 
        enter_button.clicked.connect(lambda: display_label.setText(lineedit_to_output(line_edit.text())))
        self.exit_button.clicked.connect(self.close)
        self.freq_window.freq_changed.connect(Note.set_a4)


def lineedit_to_output(s: str):
    try:
        freq = float(s)
        n, cents = Note.freq_to_note(freq)
        note_str = str(n) if n.is_natural else f"{n}/{n.enharmonic_note()}"
        return f"{note_str} ({cents:+} cents)"
    except ValueError:
        return "Invalid input." 
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()         