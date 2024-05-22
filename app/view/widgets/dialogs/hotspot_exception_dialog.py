import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget


class HotspotExceptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.buttons = QWidget()
        self.horizontalLayout = QHBoxLayout(self.buttons)
        self.setLayout(self.verticalLayout)

        self.setWindowTitle('Hotspot exception')
        self.one = QPushButton('Ok', self.buttons)
        self.one.clicked.connect(self.buttonClicked)

        self.horizontalLayout.addWidget(self.one)
        self.buttons.setLayout(self.horizontalLayout)

        self.label = QLabel(self)
        self.label.setText('Индекс интерфейса мобильной точки доступа не найден, скорее всего мобильную точку доступа '
                           'не удалось запустить.\n'
                           'Пожалуйста, включите мобильную точку доступа на Вашем ПК вручную и перезапустите приложение'
                           )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.buttons)

    def buttonClicked(self):
        self.done(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = HotspotExceptionDialog()
    dialogCode = w.exec()
    print(dialogCode)
