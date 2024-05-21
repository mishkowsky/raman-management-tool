import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget


class CheckDDWrtConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.buttons = QWidget()
        self.horizontalLayout = QHBoxLayout(self.buttons)
        self.setLayout(self.verticalLayout)

        self.setWindowTitle('Check network configuration')
        self.one = QPushButton('Ok', self.buttons)
        self.one.clicked.connect(self.buttonClicked)

        self.horizontalLayout.addWidget(self.one)
        self.buttons.setLayout(self.horizontalLayout)

        self.label = QLabel(self)
        self.label.setText('Для дальнейшей работы приложения потребуется роутер с прошивкой DD-WRT.\n'
                           'Пожалуйста, убедитесь, что ПК подключен к роутеру и IP-адрес ПК задан как 192.168.1.111\n')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.buttons)

    def buttonClicked(self):
        self.done(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CheckDDWrtConnectionDialog()
    dialogCode = w.exec()
    print(dialogCode)
