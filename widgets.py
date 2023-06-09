from PyQt6 import QtWidgets, QtCore, QtGui
from note import Note

from settings import *

class Widget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  


class MainWindowSubwidget(Widget):
    def __init__(self):
        super().__init__()
        self.vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout)

        self.vlayout.addWidget(InfoLabel())

        self.line_edit_widget = LineEditWidget()
        self.vlayout.addSpacing(4)
        self.vlayout.addWidget(self.line_edit_widget)
        self.vlayout.addSpacing(6)
        self.display_label = DisplayLabel()
        self.vlayout.addWidget(self.display_label)
        self.vlayout.itemAt(4).setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)


class Label(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


class InfoLabel(Label):
    def __init__(self):
        super().__init__()
        self.setText("Enter a frequency value in Hz to find the closest note:")


class DisplayLabel(Label):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.setFixedHeight(40)
        self.setFixedWidth(165)
        self.setFont(QtGui.QFont("Segoe UI Symbol"))
        # this font correctly displays the flat symbol
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse 
                                     | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)

    def update_upon_note_name_change(self):
        self.setText(self.text())

    @staticmethod
    def lineedit_to_label_text(s: str):
        if not s.strip():
            return ""
        try:
            freq = float(s)
            n, cents = Note.freq_to_note(freq)
            note_str = str(n) if n.is_natural else f"{n}/{n.enharmonic_note()}"
            cents_str = f" ({cents:+} cents)" if cents else ""
            return f"{note_str}{cents_str}"
        except ValueError:
            return "Invalid input."     


class PushButton(QtWidgets.QPushButton):
    def __init__(self, text: str = None):
        super().__init__()
        self.setFixedHeight(25)
        self.setFixedWidth(50)
        self.setText(text)
 

class EnterButton(PushButton):
    def __init__(self):
        super().__init__(text="Enter")


class ExitButton(PushButton):
    def __init__(self):
        super().__init__(text="Quit")


class InputLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(9)
        

class LineEditWidget(Widget):
    def __init__(self):
        super().__init__()
        self.hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout)
        self.line_edit = InputLineEdit()
        self.enter_button = EnterButton()

        self.hlayout.addSpacerItem(SpacerLarge())
        self.hlayout.addWidget(self.line_edit)
        self.hlayout.addWidget(self.enter_button)
        self.hlayout.addSpacerItem(SpacerLarge())
        self.hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(0, 0, 0, 0)


class SpacerLarge(QtWidgets.QSpacerItem):
    def __init__(self):
        super().__init__(75, 20)


class SpacerSmall(QtWidgets.QSpacerItem):
    def __init__(self):
        super().__init__(30, 20)


class FreqSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(3)
        self.setMinimum(A4_MIN)
        self.setMaximum(A4_MAX)
        self.setValue(A4_DEFAULT)
        self.setSuffix(" Hz")

    def showEvent(self, ev):
        self.setValue(Note.freq_a4)


class FreqWindow(QtWidgets.QDialog):
    freq_changed = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change reference frequency")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.vlayout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.freq_spinbox = FreqSpinBox()
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.freq_spinbox)
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.ok_button = PushButton("OK")
        self.ok_button.setDefault(True)
        self.cancel_button = PushButton("Cancel")
        self.reset_button = PushButton("Reset to default")
        self.reset_button.setFixedWidth(95)
        self.vlayout.addSpacing(12)
        self.hlayout2 = QtWidgets.QHBoxLayout()
        self.hlayout2.addSpacerItem(SpacerSmall())
        self.hlayout2.addWidget(self.reset_button)
        self.hlayout2.addWidget(self.ok_button)
        self.hlayout2.addWidget(self.cancel_button)
        self.hlayout2.addSpacerItem(SpacerSmall())
        self.vlayout.addLayout(self.hlayout2)
        self.setLayout(self.vlayout)
        self.setFixedSize(330, 100)
        self.update_upon_note_name_change()

    @property
    def current_a4(self):
        return float(self.freq_spinbox.value())
    
    @QtCore.pyqtSlot()
    def update_upon_note_name_change(self):
        self.label.setText(f"Set the frequency of {Note.note_a4()} : ")

    @QtCore.pyqtSlot()
    def emit_signal_and_close(self):
        self.freq_changed.emit(self.current_a4)
        self.close()

    @QtCore.pyqtSlot()
    def reset_freq(self):
        self.freq_spinbox.setValue(A4_DEFAULT)
