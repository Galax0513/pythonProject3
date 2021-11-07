from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt


class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet('font-size: 15px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class Use(QWidget):
    def __init__(self):
        super().__init__()

        linkTemplate = '<a href={0}>{1}</a>'

        label = HyperlinkLabel(self)
        label.setText(linkTemplate.format('https://www.youtube.com/channel/UCG-KntY7aVnIGXYEBQvmBAQ',
                                          'Канал - "Томас Франк". Всё об идельном планировании и продуктивности'))
        label.move(50, 0)

        self.pixmap = QPixmap('images.jpg')
        label_2 = QLabel(self)
        label_2.setPixmap(self.pixmap)
        label_2.move(170, 40)

        label_3 = HyperlinkLabel(self)
        label_3.setText(linkTemplate.format('https://www.youtube.com/channel/UCG-KntY7aVnIGXYEBQvmBAQ',
                                            'Ель Студия - канал, который поможет лучше узнать себя'))
        label_3.move(110, 220)

        self.pixmap1 = QPixmap('Unknown1.jpg')
        label_4 = QLabel(self)
        label_4.setPixmap(self.pixmap1)
        label_4.move(170, 260)

        label_5 = HyperlinkLabel(self)
        label_5.setText(linkTemplate.format('https://www.youtube.com/c/ПростыеМысли',
                                            'Простые мысли - поможет тебе стать лучше. Расскаже о саморазвитии, спорте и т.п.'))
        label_5.move(70, 440)

        self.pixmap2 = QPixmap('Unknown3.jpg')
        label_6 = QLabel(self)
        label_6.setPixmap(self.pixmap2)
        label_6.move(170, 480)

        pybutton = QPushButton('<--', self)
        pybutton.resize(30, 30)
        pybutton.setStyleSheet("QPushButton{   \n"
                               "background: rgb(17, 181, 206);\n"
                               " border-radius: 10px; }")
        pybutton.move(10, 10)
        pybutton.clicked.connect(self.hide_the_form1)

    """закрытие формы"""

    def hide_the_form1(self):
        self.hide()

    """горячие клавиши для выхода"""

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_D:
                self.hide_the_form1()
