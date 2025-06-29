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
    QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_dialogAction(object):
    def setupUi(self, dialogAction):
        if not dialogAction.objectName():
            dialogAction.setObjectName(u"dialogAction")
        dialogAction.resize(400, 300)
        dialogAction.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.verticalLayout = QVBoxLayout(dialogAction)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(dialogAction)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.buttonBox = QDialogButtonBox(dialogAction)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialogAction)
        self.buttonBox.accepted.connect(dialogAction.accept)
        self.buttonBox.rejected.connect(dialogAction.reject)

        QMetaObject.connectSlotsByName(dialogAction)
    # setupUi

    def retranslateUi(self, dialogAction):
        dialogAction.setWindowTitle(QCoreApplication.translate("dialogAction", u"Actions", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("dialogAction", u"\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("dialogAction", u"\u0421\u0442\u0430\u0442\u0443\u0441", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("dialogAction", u"\u0422\u0440\u0438\u0433\u0433\u0435\u0440", None));
    # retranslateUi

