# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogCreateTrigger.ui'
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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_dialogCreateTrigger(object):
    def setupUi(self, dialogCreateTrigger):
        if not dialogCreateTrigger.objectName():
            dialogCreateTrigger.setObjectName(u"dialogCreateTrigger")
        dialogCreateTrigger.resize(400, 300)
        dialogCreateTrigger.setModal(True)
        self.verticalLayout = QVBoxLayout(dialogCreateTrigger)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.whatCallLabel = QLabel(dialogCreateTrigger)
        self.whatCallLabel.setObjectName(u"whatCallLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.whatCallLabel)

        self.whatCallComboBox = QComboBox(dialogCreateTrigger)
        self.whatCallComboBox.addItem("")
        self.whatCallComboBox.setObjectName(u"whatCallComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.whatCallComboBox)

        self.frameTriggers = QFrame(dialogCreateTrigger)
        self.frameTriggers.setObjectName(u"frameTriggers")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTriggers.sizePolicy().hasHeightForWidth())
        self.frameTriggers.setSizePolicy(sizePolicy)
        self.frameTriggers.setMinimumSize(QSize(10, 20))
        self.frameTriggers.setFrameShape(QFrame.StyledPanel)
        self.frameTriggers.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.frameTriggers)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(dialogCreateTrigger)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialogCreateTrigger)
        self.buttonBox.accepted.connect(dialogCreateTrigger.accept)
        self.buttonBox.rejected.connect(dialogCreateTrigger.reject)

        QMetaObject.connectSlotsByName(dialogCreateTrigger)
    # setupUi

    def retranslateUi(self, dialogCreateTrigger):
        dialogCreateTrigger.setWindowTitle(QCoreApplication.translate("dialogCreateTrigger", u"Create Trigger", None))
        self.whatCallLabel.setText(QCoreApplication.translate("dialogCreateTrigger", u"\u041d\u0430 \u0447\u0442\u043e \u0440\u0435\u0430\u0433\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.whatCallComboBox.setItemText(0, QCoreApplication.translate("dialogCreateTrigger", u"\u041d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043e", None))

    # retranslateUi

