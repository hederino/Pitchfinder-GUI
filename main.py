import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from widgets import Widget, MainWindowSubwidget, ExitButton
from note import Note, note_a4


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

        self.quit_button_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.quit_button_layout)

        self.exit_button = ExitButton()

        self.quit_button_layout.addSpacing(self.width() - 2 * self.exit_button.width())
        self.quit_button_layout.addWidget(self.exit_button)

        self.centralWidget().setLayout(self.main_layout)

    def set_menubar(self):
        self.menubar = QtWidgets.QMenuBar()
        settings_menu = self.menubar.addMenu('&Settings')
        note_display = settings_menu.addMenu("Note names")

        # note_display.addAction()

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
        # do_re_mi.toggled.connect(self.sfw.label_a4.text_update)
        self.setMenuBar(self.menubar)

    def connect_signals(self):
        line_edit = self.main_subwidget.line_edit_widget.line_edit
        display_label = self.main_subwidget.display_label
        enter_button = self.main_subwidget.line_edit_widget.input_button 
        enter_button.clicked.connect(lambda: display_label.setText(lineedit_to_output(line_edit.text())))
        self.exit_button.clicked.connect(self.close)


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