import os

from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

from Bday import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
from bisect import bisect
import sqlite3
from PyQt5.QtCore import Qt, QUrl

MOUNTH = {"январь": 1,
          "февраль": 2,
          "март": 3,
          "апрель": 4,
          "май": 5,
          "июнь": 6,
          "июль": 7,
          "август": 8,
          "сентябрь": 9,
          "октябрь": 10,
          "ноябрь": 11,
          "декабрь": 12}

ZNACS = {"Овен": 1,
         "Телец": 2,
         "Близнецы": 3,
         "Рак": 4,
         "Лев": 5,
         "Дева": 6,
         "Весы": 7,
         "Скорпион": 8,
         "Стрелец": 9,
         "Козерог": 10,
         "Водолей": 11,
         "Рыбы": 12}

SIGNS = [(1, 20, "Козерог"), (2, 18, "Водолей"), (3, 20, "Рыбы"),
         (4, 20, "Овен"), (5, 21, "Телец"), (6, 21, "Близнецы"),
         (7, 22, "Рак"), (8, 23, "Лев"), (9, 23, "Дева"),
         (10, 23, "Весы"), (11, 22, "Скорпион"), (12, 22, "Стрелец"),
         (12, 31, "Козерог")]


class Bday(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Bday, self).__init__()
        self.setupUi(self)
        self.tableWidget_2.setColumnWidth(0, 150)
        self.tableWidget_2.setColumnWidth(1, 300)
        self.tableWidget_2.setColumnWidth(2, 180)
        self.number = [str(i + 1) for i in range(31)]
        self.comboBox_2.addItems(self.number)
        year = 2021
        self.year = [str(datetime.datetime(year - i, 1, 1)).replace('-01-01 00:00:00', '') for i in range(82)]
        self.comboBox_3.addItems(self.year)
        self.pushButton.clicked.connect(self.znac)
        self.pushButton.clicked.connect(self.add_bday_to_bd)
        self.pushButton.clicked.connect(self.load_bday)
        self.pushButton_2.setIcon(QIcon('add1.png'))
        self.pushButton_2.clicked.connect(self.delete_bday)
        self.pushButton_2.clicked.connect(self.play_audio_file)
        self.pushButton_3.clicked.connect(self.hide_the_form)
        self.player = QMediaPlayer()
        self.load_bday()

    """число, месяц, год, фамилия, имя, знак зодиака"""

    def znac(self):
        self.date_bday = self.comboBox_2.currentText()
        self.mounth_bday = self.comboBox.currentText()
        self.year_bday = self.comboBox_3.currentText()

        self.data_for_bd = self.date_bday + self.mounth_bday + self.year_bday
        self.date_of_bday = str(self.year_bday) + "-" + str(MOUNTH[self.mounth_bday]) + "-" + str(self.date_bday)
        self.name = self.lineEdit_3.text()

        self.data = datetime.datetime(int(self.year_bday), int(MOUNTH[self.mounth_bday]), int(self.date_bday))
        self.data = str(self.data).replace('00:00:00', '')

        self.m = int(MOUNTH[self.mounth_bday])
        self.d = int(self.date_bday)

        self.a = SIGNS[bisect(SIGNS, (self.m, self.d))][2]

    """добавление значений в базу данных"""

    def add_bday_to_bd(self):
        con = sqlite3.connect('birthdays.db')
        cur = con.cursor()
        result = cur.execute("""
        INSERT INTO dates_of_Bday(bday, name_sername, zodiac_sign)
        VALUES (?, ?, ?)""",
                             (str(self.data), self.lineEdit_3.text(), int(ZNACS[self.a])))
        con.commit()

    """отобразить базу данных в listwidget"""

    def load_bday(self):
        connection = sqlite3.connect("birthdays.db")
        cur = connection.cursor()
        result0 = "SELECT dates_of_Bday.bday, dates_of_Bday.name_sername, zodiacs.signs FROM dates_of_Bday " \
                  "JOIN zodiacs ON dates_of_Bday.zodiac_sign = zodiacs.id " \
                  "ORDER BY bday"

        count = "SELECT Count(id) FROM dates_of_Bday"
        res_count = cur.execute(count).fetchone()[0]

        self.tableWidget_2.setRowCount(res_count)
        table_row0 = 0
        for row in cur.execute(result0):
            self.tableWidget_2.setItem(table_row0, 0, QTableWidgetItem(row[0]))
            self.tableWidget_2.setItem(table_row0, 1, QTableWidgetItem(row[1]))
            self.tableWidget_2.setItem(table_row0, 2, QTableWidgetItem(row[2]))
            table_row0 += 1
        self.lineEdit_3.clear()
        return

    """удалить из базы данных строку выбранную"""

    def delete_bday(self):
        connection = sqlite3.connect("birthdays.db")
        cur = connection.cursor()
        content = "SELECT * FROM dates_of_Bday"
        res = cur.execute(content).fetchall()
        for row in enumerate(res):
            if row[0] == self.tableWidget_2.currentRow():
                data = row[1]
                idd = data[0]
                date_of = data[1]
                cur.execute("DELETE FROM dates_of_Bday WHERE id = (?) AND bday = (?)",
                            (idd, date_of,))
                connection.commit()
                self.load_bday()

    """скрыть форму с Дни рождения"""

    def hide_the_form(self):
        self.hide()

    """при удалении воспроизводится звук"""

    def play_audio_file(self):
        full_file_path = os.path.join(os.getcwd(), 'garbige.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    """горячие клавиши"""

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_Q:
                self.hide_the_form()
