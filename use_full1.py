import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet('font-size: 15px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()

        linkTemplate = '<a href={0}>{1}</a>'

        label_1 = HyperlinkLabel(self)
        label_1.setText(linkTemplate.format('https://www.youtube.com/c/Thomasfrank/featured', 'Канал - "Томас Франк". Всё об идельном планировании и продуктивности'))

        self.pixmap = QPixmap('images.jpg')
        label_2 = QLabel()
        label_2.setPixmap(self.pixmap)
        label_2.move(100, 100)

        label_3 = HyperlinkLabel(self)
        label_3.setText(linkTemplate.format('https://www.youtube.com/channel/UCG-KntY7aVnIGXYEBQvmBAQ', 'Ель Студия - канал, который поможет лучше узнать себя'))

        pybutton = QPushButton('Create a button', self)
        pybutton.resize(100, 100)
        pybutton.setStyleSheet("QPushButton{   \n"
                                        "background: rgb(17, 181, 206);\n"
                                        " border-radius: 10px; }")
        pybutton.move(100, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())