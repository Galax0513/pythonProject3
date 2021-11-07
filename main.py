import csv
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QListWidgetItem
from mywidget import MyWidget
from birthdays import Bday
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import *
from glav1 import Ui_MainWindow
from usefull1 import Use

conn = sqlite3.connect('mytodolist.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists todo_list(
list_item text)
""")
conn.commit()
conn.close()


class Glav(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Glav, self).__init__()
        self.setupUi(self)
        self.player = QMediaPlayer()
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 90)
        self.tableWidget.setColumnWidth(2, 250)
        self.tableWidget.setColumnWidth(3, 250)
        self.pushButton.clicked.connect(self.openDialog)
        self.pushButton_5.clicked.connect(self.delete_data)
        self.pushButton_5.clicked.connect(self.play_audio_file)
        self.pushButton_4.clicked.connect(self.load_date)
        self.pushButton_2.clicked.connect(self.todolist)
        self.pushButton_2.clicked.connect(self.save_it)
        self.pushButton_7.clicked.connect(self.delete_all_tasks)
        self.pushButton_7.clicked.connect(self.play_audio_file)
        self.pushButton_8.setIcon(QIcon('add1.png'))
        self.pushButton_8.clicked.connect(self.deleteTask)
        self.pushButton_8.clicked.connect(self.play_audio_file)
        self.pushButton_3.clicked.connect(self.openDialog2)
        self.pushButton_10.clicked.connect(self.write_csv)
        self.pushButton_11.clicked.connect(self.write_txt)
        self.pushButton_9.clicked.connect(self.getData)
        self.pushButton_6.clicked.connect(self.openDialog3)
        self.load_date()
        self.grab_all()

    """открытие окна для добавления задач"""

    def openDialog(self):
        self.dialog = MyWidget()
        self.dialog.show()

    """отображение задач"""

    def load_date(self):
        connection = sqlite3.connect("task_manager.db")
        cur = connection.cursor()
        result = "SELECT date, time, task, comments FROM tasks ORDER BY date"

        count = "SELECT Count(id) FROM tasks"
        res_count = cur.execute(count).fetchone()[0]

        self.tableWidget.setRowCount(res_count)
        table_row = 0
        for row in cur.execute(result):
            self.tableWidget.setItem(table_row, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(table_row, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(table_row, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(table_row, 3, QTableWidgetItem(row[3]))
            table_row += 1
        return

    """при изменении задачи и ком. изменить в db"""

    def getData(self):
        connection = sqlite3.connect("task_manager.db")
        cur = connection.cursor()
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                try:
                    tmp.append(self.tableWidget.item(row, col).text())
                except:
                    tmp.append('No data')
            data.append(tuple(tmp))

        for el in enumerate(data):
            if el[0] == self.tableWidget.currentRow():
                data1 = el[1]
                date1 = data1[0]
                task1 = data1[2]
                com1 = data1[3]
                cur.execute("UPDATE tasks SET task = (?), comments = (?) WHERE date = (?)",
                            (task1, com1, date1,))
                connection.commit()
                self.load_date()

    """удалить выбранную задачу"""

    def delete_data(self):
        connection = sqlite3.connect("task_manager.db")
        cur = connection.cursor()
        content = "SELECT * FROM tasks"
        res = cur.execute(content).fetchall()

        for row in enumerate(res):
            if row[0] == self.tableWidget.currentRow():
                data = row[1]
                dat = data[1]
                tas = data[3]
                cur.execute("DELETE FROM tasks WHERE date = (?) AND task = (?)", (dat, tas,))
                connection.commit()
                self.load_date()

    """из баззы данных для отображения в todolist"""

    def grab_all(self):
        conn = sqlite3.connect('mytodolist.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()
        conn.commit()
        conn.close()
        for record in records:
            if record[0]:
                taskItem = QListWidgetItem()
                taskItem.setFlags(
                    Qt.ItemIsEnabled |
                    Qt.ItemIsUserCheckable |
                    Qt.ItemIsSelectable
                )
                taskItem.setCheckState(Qt.Unchecked)
                taskItem.setText(record[0])
                self.listWidget.addItem(taskItem)

    """чтение из line edit и добавление в todolist"""

    def todolist(self):
        task = self.lineEdit.text()
        if task:
            taskItem = QListWidgetItem()
            taskItem.setFlags(
                Qt.ItemIsEnabled |
                Qt.ItemIsUserCheckable |
                Qt.ItemIsSelectable
            )
            taskItem.setCheckState(Qt.Unchecked)
            taskItem.setText(task)
            self.listWidget.addItem(taskItem)
        self.lineEdit.clear()

    """удаление выбронного задания"""

    def deleteTask(self):
        self.listWidget.takeItem(self.listWidget.row(self.listWidget.currentItem()))
        self.save_it()

    """удаление всех заданий"""

    def delete_all_tasks(self):
        self.listWidget.clear()
        self.save_it()

    """сохранить таблицу заново"""

    def save_it(self):
        conn = sqlite3.connect('mytodolist.db')
        c = conn.cursor()
        c.execute('DELETE FROM todo_list;', )

        items = []
        for index in range(self.listWidget.count()):
            items.append(self.listWidget.item(index))

        for item in items:
            c.execute("INSERT INTO todo_list VALUES (:item)",
                      {
                          'item': item.text(),
                      })
        conn.commit()
        conn.close()

    """функция для открытия окна Дни Рождения"""

    def openDialog2(self):
        self.dialog2 = Bday()
        self.dialog2.show()

    """экспорт в csv файл"""

    def write_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save File',
                                              QDir.homePath() + "/export.csv",
                                              "CSV Files(*.csv *.txt)")
        if path:
            with open(path, 'w') as stream:
                writer = csv.writer(stream, dialect='excel', delimiter=',')
                elemens = []
                for column in range(self.tableWidget.columnCount()):
                    el = self.tableWidget.horizontalHeaderItem(column)
                    if el is not None:
                        elemens.append(el.text())
                    else:
                        elemens.append("Column" + str(column))
                writer.writerow(elemens)

                for row in range(self.tableWidget.rowCount()):
                    res = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            res.append(item.text())
                        else:
                            res.append('')
                writer.writerow(res)

    """экспорт в txt файл"""

    def write_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save File',
                                              QDir.homePath() + "/export.txt",
                                              "TXT Files(*.txt)")
        if path:
            with open(path, 'w') as stream:
                for row in range(self.tableWidget.rowCount()):
                    res = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            res.append(item.text())
                        else:
                            res.append('')
                    stream.write(' '.join(res) + '\n' + '-------------------------------' + '\n')

    """при удалении воспроизводится звук"""

    def play_audio_file(self):
        full_file_path = os.path.join(os.getcwd(), 'garbige.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    """горячие клавиши"""

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.openDialog()
        elif event.key() == Qt.Key_F6:
            self.openDialog2()
        elif int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_A:
                self.load_date()
            elif event.key() == Qt.Key_C:
                self.write_csv()
            elif event.key() == Qt.Key_T:
                self.write_txt()

    """показывает Полезные ссылки"""

    def openDialog3(self):
        self.dialog3 = Use()
        self.dialog3.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Glav()
    ex.show()
    sys.exit(app.exec())
