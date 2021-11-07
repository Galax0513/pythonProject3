from PyQt5.QtWidgets import QMainWindow
from task_write1 import Ui_MainWindow
import sqlite3


class MyWidget(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.values)
        self.pushButton_2.clicked.connect(self.add_to_bd)
        self.pushButton_2.clicked.connect(self.hide)

    """значения: дата, время, задача, комментарии"""

    def values(self):
        self.start_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.time = self.timeEdit.time().toString('hh:mm')
        self.line_edit1 = self.lineEdit.text()
        self.line_edit2 = self.lineEdit_2.text()

    """добавление в базу данных задач"""

    def add_to_bd(self):
        con = sqlite3.connect('task_manager.db')
        cur = con.cursor()
        result = cur.execute("""
        INSERT INTO tasks(date, time, task, comments)
        VALUES (?, ?, ?, ?)""", (self.start_date, self.time, self.line_edit1, self.line_edit2))
        con.commit()
