import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget


class FirewallExceptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.buttons = QWidget()
        self.horizontalLayout = QHBoxLayout(self.buttons)
        self.setLayout(self.verticalLayout)

        self.setWindowTitle('Firewall exception')
        self.one = QPushButton('Ok', self.buttons)
        self.one.clicked.connect(self.buttonClicked)

        self.horizontalLayout.addWidget(self.one)
        self.buttons.setLayout(self.horizontalLayout)

        self.label = QLabel(self)
        self.label.setText('Произошла ошибка при запуске firewall\'a. \n'
                           'Для дальнейшей работы приложения потребуется роутер с прошивкой DD-WRT.\n'
                           'Пожалуйста, убедитесь, что ПК подключен к роутеру и IP-адрес ПК задан как 192.168.1.111\n'
                           'Либо перезапустите приложение, подобная ошибка может быть связана с первым запуском '
                           'приложения на данном ПК и может не появиться при запуске во второй раз.')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.buttons)

    def close(self):
        self.setResult(QDialog.DialogCode.Rejected)
        self.reject()
        # self.done(0)

    def buttonClicked(self):
        self.setResult(QDialog.DialogCode.Accepted)
        self.accept()
        # self.done(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FirewallExceptionDialog()
    dialogCode = w.exec()
    if not dialogCode:
        sys.exit()
    res = w.accepted
    print(w.result())
    print(dialogCode)
