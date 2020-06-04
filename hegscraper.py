# Tool zur Rechnereinbindung in Iserv
# (c) 2020 by Dietrich Poensgen

# Imports für GUI
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QGridLayout, QLineEdit, QMessageBox, QComboBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

# Imports für automatische Website-Interaktion
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenstergröße und Fenstertitel
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle('IServ-Login')

        # Fenster-Icon (Iserv)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'icon.png'))

        # Formular-Widget
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)

        # Formular-Beschriftung
        row = 0
        beschriftung = ['Accountname:', 'Passwort:', ]
        beschriftunglaenge = len(beschriftung)

        for s in beschriftung:
            lbl = QLabel(s)
            lbl.resize(lbl.sizeHint())
            grid.addWidget(lbl, row, 1, QtCore.Qt.AlignRight)

            row += 1

        # Formular-Felder
        self.accountnameFeld = QLineEdit(self)
        grid.addWidget(self.accountnameFeld, 0, 2,   QtCore.Qt.AlignLeft)

        self.passwortFeld = QLineEdit(self)
        self.passwortFeld.setEchoMode(QLineEdit.Password)
        grid.addWidget(self.passwortFeld, 1, 2,   QtCore.Qt.AlignLeft)

        # Abschick-Button
        abschicken = QPushButton('Abschicken', self)
        abschicken.clicked.connect(self.ausfuehren)
        grid.addWidget(abschicken, 3, 3,)

        # Abbrech/Beenden-Button
        abbrechen = QPushButton('Abbrechen', self)
        abbrechen.clicked.connect(self.abbruch)
        grid.addWidget(abbrechen, 3, 0,)

    # Methode, die die Aktion des Abschick-Buttons ist
    def ausfuehren(self):

        # Absicherung gegen nicht angegebene Login-Daten
        if self.accountnameFeld.text() == '':
            QMessageBox.about(
                self, 'Fehler!', 'Bitte geben sie einen Benutzernamen an')
            return
        if self.passwortFeld.text() == '':
            QMessageBox.about(
                self, 'Fehler!', 'Bitte geben sie ein Passwort an')
            return

        # Die in das UI eingepflegten Daten werden zu Variabeln konvertiert
        # Login-Data
        user_name = self.accountnameFeld.text()
        password = self.passwortFeld.text()

        # Start des Browsers; damit beginnt das Einpflegen der Daten
        driver = webdriver.Firefox()
        driver.get("https://heg-portal.de/iserv/mail")

        # Login
        element = driver.find_element_by_name("_username")
        element.send_keys(user_name)
        element = driver.find_element_by_name("_password")
        element.send_keys(password)
        element.send_keys(Keys.RETURN)

        # Abruf der Nachrichten-Anzahl
        emailmenu = driver.find_element_by_class_name(
            "panel panel-default mb0 mailboxes")
        emailzahl = emailmenu.find_element_by_class_name("text-right badge")
        QMessageBox.about(self, 'E-Mails', 'Du hast ' +
                          emailzahl + ' E-Mails.')

    # Methode, die die Aktion des Abbrechen-Buttons ist

    def abbruch(self):
        sys.exit(app.exec_())


app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())
