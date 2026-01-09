# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogCreateAction.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QFrame, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_dialogCreateAction(object):
    def setupUi(self, dialogCreateAction):
        if not dialogCreateAction.objectName():
            dialogCreateAction.setObjectName(u"dialogCreateAction")
        dialogCreateAction.setWindowModality(Qt.WindowModal)
        dialogCreateAction.resize(400, 300)
        self.verticalLayout = QVBoxLayout(dialogCreateAction)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.whatCallLabel = QLabel(dialogCreateAction)
        self.whatCallLabel.setObjectName(u"whatCallLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.whatCallLabel)

        self.whatCallComboBox = QComboBox(dialogCreateAction)
        self.whatCallComboBox.addItem("")
        self.whatCallComboBox.setObjectName(u"whatCallComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.whatCallComboBox)

        self.btnCreateTrigger = QPushButton(dialogCreateAction)
        self.btnCreateTrigger.setObjectName(u"btnCreateTrigger")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.btnCreateTrigger)

        self.listTriggers = QListWidget(dialogCreateAction)
        self.listTriggers.setObjectName(u"listTriggers")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.listTriggers)

        self.frameActions = QFrame(dialogCreateAction)
        self.frameActions.setObjectName(u"frameActions")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameActions.sizePolicy().hasHeightForWidth())
        self.frameActions.setSizePolicy(sizePolicy)
        self.frameActions.setMinimumSize(QSize(10, 20))
        self.frameActions.setFrameShape(QFrame.StyledPanel)
        self.frameActions.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.frameActions)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(dialogCreateAction)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialogCreateAction)
        self.buttonBox.accepted.connect(dialogCreateAction.accept)
        self.buttonBox.rejected.connect(dialogCreateAction.reject)

        self.whatCallComboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialogCreateAction)
    # setupUi

    def retranslateUi(self, dialogCreateAction):
        dialogCreateAction.setWindowTitle(QCoreApplication.translate("dialogCreateAction", u"Create Action", None))
        self.whatCallLabel.setText(QCoreApplication.translate("dialogCreateAction", u"\u0427\u0442\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0442\u044c", None))
        self.whatCallComboBox.setItemText(0, QCoreApplication.translate("dialogCreateAction", u"\u041d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043e", None))

        self.btnCreateTrigger.setText(QCoreApplication.translate("dialogCreateAction", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0440\u0438\u0433\u0433\u0435\u0440", None))
    # retranslateUi

