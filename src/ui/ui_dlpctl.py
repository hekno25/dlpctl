# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlpctlySppoX.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1135, 957)
        MainWindow.setIconSize(QSize(30, 30))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalFrame_2 = QFrame(self.centralwidget)
        self.horizontalFrame_2.setObjectName(u"horizontalFrame_2")
        self.horizontalFrame_2.setMouseTracking(True)
        self.horizontalFrame_2.setAutoFillBackground(False)
        self.horizontalFrame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.video_layout = QVBoxLayout()
        self.video_layout.setObjectName(u"video_layout")
        self.label = QLabel(self.horizontalFrame_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        self.video_layout.addWidget(self.label)

        self.video_frame = QLabel(self.horizontalFrame_2)
        self.video_frame.setObjectName(u"video_frame")

        self.video_layout.addWidget(self.video_frame)

        self.line_2 = QFrame(self.horizontalFrame_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.video_layout.addWidget(self.line_2)

        self.line_3 = QFrame(self.horizontalFrame_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.video_layout.addWidget(self.line_3)

        self.video_slider = QSlider(self.horizontalFrame_2)
        self.video_slider.setObjectName(u"video_slider")
        self.video_slider.setOrientation(Qt.Orientation.Horizontal)

        self.video_layout.addWidget(self.video_slider)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.play = QPushButton(self.horizontalFrame_2)
        self.play.setObjectName(u"play")

        self.horizontalLayout.addWidget(self.play)

        self.pause = QPushButton(self.horizontalFrame_2)
        self.pause.setObjectName(u"pause")

        self.horizontalLayout.addWidget(self.pause)

        self.replay = QPushButton(self.horizontalFrame_2)
        self.replay.setObjectName(u"replay")

        self.horizontalLayout.addWidget(self.replay)

        self.capture = QPushButton(self.horizontalFrame_2)
        self.capture.setObjectName(u"capture")

        self.horizontalLayout.addWidget(self.capture)

        self.pushButton = QPushButton(self.horizontalFrame_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.horizontalFrame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.video_layout.addLayout(self.horizontalLayout)

        self.video_layout.setStretch(0, 1)

        self.horizontalLayout_2.addLayout(self.video_layout)

        self.line = QFrame(self.horizontalFrame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.tool_layout = QVBoxLayout()
        self.tool_layout.setObjectName(u"tool_layout")
        self.tool_label = QLabel(self.horizontalFrame_2)
        self.tool_label.setObjectName(u"tool_label")
        self.tool_label.setFont(font)

        self.tool_layout.addWidget(self.tool_label)

        self.line_4 = QFrame(self.horizontalFrame_2)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.tool_layout.addWidget(self.line_4)

        self.tabWidget = QTabWidget(self.horizontalFrame_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.video_filters = QWidget()
        self.video_filters.setObjectName(u"video_filters")
        self.verticalLayout_3 = QVBoxLayout(self.video_filters)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.video_filters)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.radioButton = QRadioButton(self.video_filters)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout.addWidget(self.radioButton, 0, 1, 1, 1)

        self.horizontalSlider = QSlider(self.video_filters)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider, 1, 0, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.video_filters)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.video_filters)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_3.addWidget(self.radioButton_2, 0, 1, 1, 1)

        self.horizontalSlider_2 = QSlider(self.video_filters)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider_2, 1, 0, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.video_filters)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)

        self.radioButton_3 = QRadioButton(self.video_filters)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_4.addWidget(self.radioButton_3, 0, 1, 1, 1)

        self.horizontalSlider_3 = QSlider(self.video_filters)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_3, 1, 0, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout_4)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_5 = QLabel(self.video_filters)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)

        self.radioButton_4 = QRadioButton(self.video_filters)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_5.addWidget(self.radioButton_4, 0, 1, 1, 1)

        self.horizontalSlider_4 = QSlider(self.video_filters)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_4, 1, 0, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout_5)

        self.tabWidget.addTab(self.video_filters, "")
        self.drawing = QWidget()
        self.drawing.setObjectName(u"drawing")
        self.verticalLayout_2 = QVBoxLayout(self.drawing)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.tabWidget.addTab(self.drawing, "")

        self.tool_layout.addWidget(self.tabWidget)

        self.tool_layout.setStretch(0, 1)
        self.tool_layout.setStretch(2, 27)

        self.horizontalLayout_2.addLayout(self.tool_layout)

        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(2, 4)

        self.verticalLayout.addWidget(self.horizontalFrame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1135, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.video_frame.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.play.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.replay.setText(QCoreApplication.translate("MainWindow", u"Replay", None))
        self.capture.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect Camera", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Connect DLP", None))
        self.tool_label.setText(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"OpenCV Filter", None))
        self.radioButton.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"OpenCV Filter", None))
        self.radioButton_2.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"OpenCV Filter", None))
        self.radioButton_3.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"OpenCV Filter", None))
        self.radioButton_4.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.video_filters), QCoreApplication.translate("MainWindow", u"Video Filters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.drawing), QCoreApplication.translate("MainWindow", u"Drawing", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

