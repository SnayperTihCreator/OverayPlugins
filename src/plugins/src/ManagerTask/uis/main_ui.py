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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListView,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

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
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        ManagerTask.setFont(font)
        self.verticalLayout = QVBoxLayout(ManagerTask)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ManagerTask)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listView = QListView(ManagerTask)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout_2.addWidget(self.listView)


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
        self.btnCreateTask.setText(QCoreApplication.translate("ManagerTask", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
    # retranslateUi

