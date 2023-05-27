from PyQt6 import QtWidgets, QtCore, QtGui

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  


class MainWindowSubwidget(Widget):
    def __init__(self):
        super().__init__()
        self.vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout)

        self.vlayout.addWidget(InfoLabel())

        self.line_edit_widget = LineEditWidget()
        self.vlayout.addSpacing(8)
        self.vlayout.addWidget(self.line_edit_widget)
        self.vlayout.addSpacing(16)
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
        self.setFont(QtGui.QFont("Segoe UI Symbol")) # this font correctly displays the flat symbol 


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
        

class LineEditWidget(Widget):
    def __init__(self):
        super().__init__()
        self.hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout)
        self.line_edit = InputLineEdit()
        self.input_button = EnterButton()

        self.hlayout.addSpacerItem(Spacer())
        self.hlayout.addWidget(self.line_edit)
        self.hlayout.addWidget(self.input_button)
        self.hlayout.addSpacerItem(Spacer())
        self.hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(0, 0, 0, 0)


class Spacer(QtWidgets.QSpacerItem):
    def __init__(self):
        super().__init__(75, 20)


class FreqSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(3)
        self.setMinimum(400.0)  # consts
        self.setMaximum(500.0)
        self.setValue(440.0)
        # self.setFixedWidth(80)
        self.setSuffix(" Hz")
