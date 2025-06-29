# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogCreateTask.ui'
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
    QFormLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_dialogCreateTask(object):
    def setupUi(self, dialogCreateTask):
        if not dialogCreateTask.objectName():
            dialogCreateTask.setObjectName(u"dialogCreateTask")
        dialogCreateTask.setWindowModality(Qt.ApplicationModal)
        dialogCreateTask.resize(400, 300)
        self.verticalLayout = QVBoxLayout(dialogCreateTask)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.nameLabel = QLabel(dialogCreateTask)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(dialogCreateTask)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.nameLineEdit)

        self.listActions = QListWidget(dialogCreateTask)
        self.listActions.setObjectName(u"listActions")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.listActions)

        self.btnCreateAction = QPushButton(dialogCreateTask)
        self.btnCreateAction.setObjectName(u"btnCreateAction")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.btnCreateAction)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(dialogCreateTask)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialogCreateTask)
        self.buttonBox.accepted.connect(dialogCreateTask.accept)
        self.buttonBox.rejected.connect(dialogCreateTask.reject)

        QMetaObject.connectSlotsByName(dialogCreateTask)
    # setupUi

    def retranslateUi(self, dialogCreateTask):
        dialogCreateTask.setWindowTitle(QCoreApplication.translate("dialogCreateTask", u"Create Task", None))
        self.nameLabel.setText(QCoreApplication.translate("dialogCreateTask", u"\u0418\u043c\u044f", None))
        self.btnCreateAction.setText(QCoreApplication.translate("dialogCreateTask", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435", None))
    # retranslateUi

