# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogActions.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QListView, QSizePolicy, QVBoxLayout, QWidget)

class Ui_dialogAction(object):
    def setupUi(self, dialogAction):
        if not dialogAction.objectName():
            dialogAction.setObjectName(u"dialogAction")
        dialogAction.resize(600, 300)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        dialogAction.setFont(font)
        dialogAction.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.verticalLayout = QVBoxLayout(dialogAction)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listView = QListView(dialogAction)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)

        self.buttonBox = QDialogButtonBox(dialogAction)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialogAction)
        self.buttonBox.accepted.connect(dialogAction.accept)
        self.buttonBox.rejected.connect(dialogAction.reject)

        QMetaObject.connectSlotsByName(dialogAction)
    # setupUi

    def retranslateUi(self, dialogAction):
        dialogAction.setWindowTitle(QCoreApplication.translate("dialogAction", u"Actions", None))
    # retranslateUi

