# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_ManagerTask(object):
    def setupUi(self, ManagerTask):
        if not ManagerTask.objectName():
            ManagerTask.setObjectName(u"ManagerTask")
        ManagerTask.resize(426, 344)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ManagerTask.sizePolicy().hasHeightForWidth())
        ManagerTask.setSizePolicy(sizePolicy)
        ManagerTask.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(ManagerTask)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ManagerTask)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableWidget = QTableWidget(ManagerTask)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.tableWidget)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.btnCreateTask = QPushButton(ManagerTask)
        self.btnCreateTask.setObjectName(u"btnCreateTask")

        self.verticalLayout.addWidget(self.btnCreateTask)


        self.retranslateUi(ManagerTask)

        QMetaObject.connectSlotsByName(ManagerTask)
    # setupUi

    def retranslateUi(self, ManagerTask):
        ManagerTask.setWindowTitle(QCoreApplication.translate("ManagerTask", u"ManagerTask", None))
        self.label.setText(QCoreApplication.translate("ManagerTask", u"Manager Task", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ManagerTask", u"UID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ManagerTask", u"\u0418\u043c\u044f", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ManagerTask", u"\u0421\u0442\u0430\u0442\u0443\u0441", None));
        self.btnCreateTask.setText(QCoreApplication.translate("ManagerTask", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
    # retranslateUi

