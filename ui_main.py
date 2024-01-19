# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainKnEUbV.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QCommandLinkButton, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPlainTextEdit, QPushButton, QRadioButton,
    QScrollArea, QScrollBar, QSizePolicy, QSlider,
    QStackedWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1303, 727)
        MainWindow.setMinimumSize(QSize(940, 727))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"TextEdit */\n"
"QTextEdit {\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-file.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-library-add.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        self.btn_swat = QPushButton(self.topMenu)
        self.btn_swat.setObjectName(u"btn_swat")
        sizePolicy.setHeightForWidth(self.btn_swat.sizePolicy().hasHeightForWidth())
        self.btn_swat.setSizePolicy(sizePolicy)
        self.btn_swat.setMinimumSize(QSize(0, 45))
        self.btn_swat.setFont(font)
        self.btn_swat.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_swat.setLayoutDirection(Qt.LeftToRight)
        self.btn_swat.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-terminal.png);")

        self.verticalLayout_8.addWidget(self.btn_swat)

        self.btn_computer = QPushButton(self.topMenu)
        self.btn_computer.setObjectName(u"btn_computer")
        self.btn_computer.setMinimumSize(QSize(0, 45))
        self.btn_computer.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-devices.png);")

        self.verticalLayout_8.addWidget(self.btn_computer)

        # self.btn_exit = QPushButton(self.topMenu)
        # self.btn_exit.setObjectName(u"btn_exit")
        # sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        # self.btn_exit.setSizePolicy(sizePolicy)
        # self.btn_exit.setMinimumSize(QSize(0, 45))
        # self.btn_exit.setFont(font)
        # self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        # self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        # self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"btn_share")
        sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LeftToRight)
        self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        self.verticalLayout_11.addWidget(self.btn_share)

        self.btn_adjustments = QPushButton(self.extraTopMenu)
        self.btn_adjustments.setObjectName(u"btn_adjustments")
        sizePolicy.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        self.btn_adjustments.setSizePolicy(sizePolicy)
        self.btn_adjustments.setMinimumSize(QSize(0, 45))
        self.btn_adjustments.setFont(font)
        self.btn_adjustments.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_adjustments.setLayoutDirection(Qt.LeftToRight)
        self.btn_adjustments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-equalizer.png);")

        self.verticalLayout_11.addWidget(self.btn_adjustments)

        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setObjectName(u"btn_more")
        sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LeftToRight)
        self.btn_more.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")

        self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.btn_home_2 = QPushButton(self.home)
        self.btn_home_2.setObjectName(u"btn_home_2")
        self.btn_home_2.setGeometry(QRect(10, 10, 61, 51))
        sizePolicy.setHeightForWidth(self.btn_home_2.sizePolicy().hasHeightForWidth())
        self.btn_home_2.setSizePolicy(sizePolicy)
        self.btn_home_2.setMinimumSize(QSize(0, 45))
        self.btn_home_2.setFont(font)
        self.btn_home_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home_2.setLayoutDirection(Qt.LeftToRight)
        self.btn_home_2.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-folder-open.png);")
        icon4 = QIcon()
        icon4.addFile(u"images/icons/PDF.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_home_2.setIcon(icon4)
        self.btn_home_2.setIconSize(QSize(25, 25))
        self.btn_home_3 = QPushButton(self.home)
        self.btn_home_3.setObjectName(u"btn_home_3")
        self.btn_home_3.setGeometry(QRect(10, 70, 61, 51))
        sizePolicy.setHeightForWidth(self.btn_home_3.sizePolicy().hasHeightForWidth())
        self.btn_home_3.setSizePolicy(sizePolicy)
        self.btn_home_3.setMinimumSize(QSize(0, 45))
        self.btn_home_3.setFont(font)
        self.btn_home_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home_3.setLayoutDirection(Qt.LeftToRight)
        self.btn_home_3.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-folder-open.png);")
        icon5 = QIcon()
        icon5.addFile(u"images/icons/DOC.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_home_3.setIcon(icon5)
        self.btn_home_3.setIconSize(QSize(25, 25))
        self.btn_prepare = QPushButton(self.home)
        self.btn_prepare.setObjectName(u"btn_prepare")
        self.btn_prepare.setGeometry(QRect(10, 130, 61, 51))
        sizePolicy.setHeightForWidth(self.btn_prepare.sizePolicy().hasHeightForWidth())
        self.btn_prepare.setSizePolicy(sizePolicy)
        self.btn_prepare.setMinimumSize(QSize(0, 45))
        self.btn_prepare.setFont(font)
        self.btn_prepare.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_prepare.setLayoutDirection(Qt.LeftToRight)
        self.btn_prepare.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-folder-open.png);")
        icon6 = QIcon()
        icon6.addFile(u"images/icons/prepare.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_prepare.setIcon(icon6)
        self.btn_prepare.setIconSize(QSize(25, 25))
        self.btn_analysis = QPushButton(self.home)
        self.btn_analysis.setObjectName(u"btn_analysis")
        self.btn_analysis.setGeometry(QRect(10, 190, 61, 51))
        sizePolicy.setHeightForWidth(self.btn_analysis.sizePolicy().hasHeightForWidth())
        self.btn_analysis.setSizePolicy(sizePolicy)
        self.btn_analysis.setMinimumSize(QSize(0, 45))
        self.btn_analysis.setFont(font)
        self.btn_analysis.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_analysis.setLayoutDirection(Qt.LeftToRight)
        self.btn_analysis.setStyleSheet(u"background-image: url(:/icons/images/icons/PDF.png);")
        icon7 = QIcon()
        icon7.addFile(u"images/icons/analysis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_analysis.setIcon(icon7)
        self.btn_analysis.setIconSize(QSize(25, 25))
        self.stackedWidget.addWidget(self.home)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.gridLayout = QGridLayout(self.widgets)
        self.gridLayout.setObjectName(u"gridLayout")
        self.row_1 = QFrame(self.widgets)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setEnabled(True)
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.row_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.row_1)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, -438, 1153, 1000))
        self.scrollAreaWidgetContents_4.setMinimumSize(QSize(0, 1000))
        self.pushButton_01 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_01.setObjectName(u"pushButton_01")
        self.pushButton_01.setGeometry(QRect(870, 40, 150, 30))
        self.pushButton_01.setMinimumSize(QSize(150, 30))
        self.pushButton_01.setFont(font)
        self.pushButton_01.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_01.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_01.setIcon(icon4)
        self.labelBoxBlenderInstalation_1 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_1.setObjectName(u"labelBoxBlenderInstalation_1")
        self.labelBoxBlenderInstalation_1.setGeometry(QRect(20, 10, 211, 21))
        self.labelBoxBlenderInstalation_1.setFont(font)
        self.labelBoxBlenderInstalation_1.setStyleSheet(u"")
        self.lineEdit_01 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_01.setObjectName(u"lineEdit_01")
        self.lineEdit_01.setGeometry(QRect(10, 40, 791, 30))
        self.lineEdit_01.setMinimumSize(QSize(0, 30))
        self.lineEdit_01.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_02 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_02.setObjectName(u"pushButton_02")
        self.pushButton_02.setGeometry(QRect(870, 110, 150, 30))
        self.pushButton_02.setMinimumSize(QSize(150, 30))
        self.pushButton_02.setFont(font)
        self.pushButton_02.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_02.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_02.setIcon(icon4)
        self.labelBoxBlenderInstalation_2 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_2.setObjectName(u"labelBoxBlenderInstalation_2")
        self.labelBoxBlenderInstalation_2.setGeometry(QRect(20, 80, 341, 21))
        self.labelBoxBlenderInstalation_2.setFont(font)
        self.labelBoxBlenderInstalation_2.setStyleSheet(u"")
        self.lineEdit_02 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_02.setObjectName(u"lineEdit_02")
        self.lineEdit_02.setGeometry(QRect(10, 110, 791, 30))
        self.lineEdit_02.setMinimumSize(QSize(0, 30))
        self.lineEdit_02.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_04 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_04.setObjectName(u"pushButton_04")
        self.pushButton_04.setGeometry(QRect(870, 250, 150, 30))
        self.pushButton_04.setMinimumSize(QSize(150, 30))
        self.pushButton_04.setFont(font)
        self.pushButton_04.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_04.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_04.setIcon(icon4)
        self.pushButton_03 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_03.setObjectName(u"pushButton_03")
        self.pushButton_03.setGeometry(QRect(870, 180, 150, 30))
        self.pushButton_03.setMinimumSize(QSize(150, 30))
        self.pushButton_03.setFont(font)
        self.pushButton_03.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_03.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_03.setIcon(icon4)
        self.labelBoxBlenderInstalation_4 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_4.setObjectName(u"labelBoxBlenderInstalation_4")
        self.labelBoxBlenderInstalation_4.setGeometry(QRect(20, 220, 211, 21))
        self.labelBoxBlenderInstalation_4.setFont(font)
        self.labelBoxBlenderInstalation_4.setStyleSheet(u"")
        self.lineEdit_04 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_04.setObjectName(u"lineEdit_04")
        self.lineEdit_04.setGeometry(QRect(10, 250, 791, 30))
        self.lineEdit_04.setMinimumSize(QSize(0, 30))
        self.lineEdit_04.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.labelBoxBlenderInstalation_3 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_3.setObjectName(u"labelBoxBlenderInstalation_3")
        self.labelBoxBlenderInstalation_3.setGeometry(QRect(20, 150, 151, 21))
        self.labelBoxBlenderInstalation_3.setFont(font)
        self.labelBoxBlenderInstalation_3.setStyleSheet(u"")
        self.lineEdit_03 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_03.setObjectName(u"lineEdit_03")
        self.lineEdit_03.setGeometry(QRect(10, 180, 791, 30))
        self.lineEdit_03.setMinimumSize(QSize(0, 30))
        self.lineEdit_03.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_06 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_06.setObjectName(u"pushButton_06")
        self.pushButton_06.setGeometry(QRect(870, 390, 150, 30))
        self.pushButton_06.setMinimumSize(QSize(150, 30))
        self.pushButton_06.setFont(font)
        self.pushButton_06.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_06.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_06.setIcon(icon4)
        self.pushButton_05 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_05.setObjectName(u"pushButton_05")
        self.pushButton_05.setGeometry(QRect(870, 320, 150, 30))
        self.pushButton_05.setMinimumSize(QSize(150, 30))
        self.pushButton_05.setFont(font)
        self.pushButton_05.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_05.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_05.setIcon(icon4)
        self.labelBoxBlenderInstalation_6 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_6.setObjectName(u"labelBoxBlenderInstalation_6")
        self.labelBoxBlenderInstalation_6.setGeometry(QRect(20, 360, 291, 16))
        self.labelBoxBlenderInstalation_6.setFont(font)
        self.labelBoxBlenderInstalation_6.setStyleSheet(u"")
        self.lineEdit_06 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_06.setObjectName(u"lineEdit_06")
        self.lineEdit_06.setGeometry(QRect(10, 390, 791, 30))
        self.lineEdit_06.setMinimumSize(QSize(0, 30))
        self.lineEdit_06.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.labelBoxBlenderInstalation_5 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_5.setObjectName(u"labelBoxBlenderInstalation_5")
        self.labelBoxBlenderInstalation_5.setGeometry(QRect(20, 290, 191, 21))
        self.labelBoxBlenderInstalation_5.setFont(font)
        self.labelBoxBlenderInstalation_5.setStyleSheet(u"")
        self.lineEdit_05 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_05.setObjectName(u"lineEdit_05")
        self.lineEdit_05.setGeometry(QRect(10, 320, 791, 30))
        self.lineEdit_05.setMinimumSize(QSize(0, 30))
        self.lineEdit_05.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_08 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_08.setObjectName(u"pushButton_08")
        self.pushButton_08.setGeometry(QRect(870, 530, 150, 30))
        self.pushButton_08.setMinimumSize(QSize(150, 30))
        self.pushButton_08.setFont(font)
        self.pushButton_08.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_08.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_08.setIcon(icon4)
        self.pushButton_07 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_07.setObjectName(u"pushButton_07")
        self.pushButton_07.setGeometry(QRect(870, 460, 150, 30))
        self.pushButton_07.setMinimumSize(QSize(150, 30))
        self.pushButton_07.setFont(font)
        self.pushButton_07.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_07.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_07.setIcon(icon4)
        self.labelBoxBlenderInstalation_8 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_8.setObjectName(u"labelBoxBlenderInstalation_8")
        self.labelBoxBlenderInstalation_8.setGeometry(QRect(20, 500, 221, 21))
        self.labelBoxBlenderInstalation_8.setFont(font)
        self.labelBoxBlenderInstalation_8.setStyleSheet(u"")
        self.lineEdit_08 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_08.setObjectName(u"lineEdit_08")
        self.lineEdit_08.setGeometry(QRect(10, 530, 791, 30))
        self.lineEdit_08.setMinimumSize(QSize(0, 30))
        self.lineEdit_08.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.labelBoxBlenderInstalation_7 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_7.setObjectName(u"labelBoxBlenderInstalation_7")
        self.labelBoxBlenderInstalation_7.setGeometry(QRect(20, 430, 241, 21))
        self.labelBoxBlenderInstalation_7.setFont(font)
        self.labelBoxBlenderInstalation_7.setStyleSheet(u"")
        self.lineEdit_07 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_07.setObjectName(u"lineEdit_07")
        self.lineEdit_07.setGeometry(QRect(10, 460, 791, 30))
        self.lineEdit_07.setMinimumSize(QSize(0, 30))
        self.lineEdit_07.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.lineEdit_10 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setGeometry(QRect(10, 670, 791, 30))
        self.lineEdit_10.setMinimumSize(QSize(0, 30))
        self.lineEdit_10.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.lineEdit_12 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setGeometry(QRect(10, 810, 791, 30))
        self.lineEdit_12.setMinimumSize(QSize(0, 30))
        self.lineEdit_12.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_10 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(870, 670, 150, 30))
        self.pushButton_10.setMinimumSize(QSize(150, 30))
        self.pushButton_10.setFont(font)
        self.pushButton_10.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_10.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_10.setIcon(icon4)
        self.labelBoxBlenderInstalation_10 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_10.setObjectName(u"labelBoxBlenderInstalation_10")
        self.labelBoxBlenderInstalation_10.setGeometry(QRect(20, 640, 371, 16))
        self.labelBoxBlenderInstalation_10.setFont(font)
        self.labelBoxBlenderInstalation_10.setStyleSheet(u"")
        self.labelBoxBlenderInstalation_11 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_11.setObjectName(u"labelBoxBlenderInstalation_11")
        self.labelBoxBlenderInstalation_11.setGeometry(QRect(20, 720, 271, 16))
        self.labelBoxBlenderInstalation_11.setFont(font)
        self.labelBoxBlenderInstalation_11.setStyleSheet(u"")
        self.pushButton_09 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_09.setObjectName(u"pushButton_09")
        self.pushButton_09.setGeometry(QRect(870, 600, 150, 30))
        self.pushButton_09.setMinimumSize(QSize(150, 30))
        self.pushButton_09.setFont(font)
        self.pushButton_09.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_09.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_09.setIcon(icon4)
        self.lineEdit_09 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_09.setObjectName(u"lineEdit_09")
        self.lineEdit_09.setGeometry(QRect(10, 600, 791, 30))
        self.lineEdit_09.setMinimumSize(QSize(0, 30))
        self.lineEdit_09.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.lineEdit_11 = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setGeometry(QRect(10, 740, 791, 30))
        self.lineEdit_11.setMinimumSize(QSize(0, 30))
        self.lineEdit_11.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pushButton_12 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(870, 810, 150, 30))
        self.pushButton_12.setMinimumSize(QSize(150, 30))
        self.pushButton_12.setFont(font)
        self.pushButton_12.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_12.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_12.setIcon(icon4)
        self.labelBoxBlenderInstalation_12 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_12.setObjectName(u"labelBoxBlenderInstalation_12")
        self.labelBoxBlenderInstalation_12.setGeometry(QRect(20, 790, 191, 16))
        self.labelBoxBlenderInstalation_12.setFont(font)
        self.labelBoxBlenderInstalation_12.setStyleSheet(u"")
        self.pushButton_11 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(870, 740, 150, 30))
        self.pushButton_11.setMinimumSize(QSize(150, 30))
        self.pushButton_11.setFont(font)
        self.pushButton_11.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_11.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_11.setIcon(icon4)
        self.labelBoxBlenderInstalation_9 = QLabel(self.scrollAreaWidgetContents_4)
        self.labelBoxBlenderInstalation_9.setObjectName(u"labelBoxBlenderInstalation_9")
        self.labelBoxBlenderInstalation_9.setGeometry(QRect(20, 570, 311, 21))
        self.labelBoxBlenderInstalation_9.setFont(font)
        self.labelBoxBlenderInstalation_9.setStyleSheet(u"")
        self.pushButton_13 = QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(20, 870, 150, 31))
        self.pushButton_13.setMinimumSize(QSize(150, 30))
        self.pushButton_13.setFont(font)
        self.pushButton_13.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_13.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_13.setIcon(icon5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.row_1, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.widgets)
        self.runswat = QWidget()
        self.runswat.setObjectName(u"runswat")
        self.gridLayout_7 = QGridLayout(self.runswat)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.textEdit_2 = QTextEdit(self.runswat)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setStyleSheet("color: black; background-color: rgb(52, 59, 72);")

        self.gridLayout_7.addWidget(self.textEdit_2, 0, 0, 1, 2)

        self.textEdit_3 = QTextEdit(self.runswat)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setStyleSheet("color: black; background-color: rgb(52, 59, 72);")

        self.gridLayout_7.addWidget(self.textEdit_3, 0, 2, 1, 1)

        self.pushButton_21 = QPushButton(self.runswat)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setMinimumSize(QSize(150, 30))
        self.pushButton_21.setFont(font)
        self.pushButton_21.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_21.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/cil-terminal.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_21.setIcon(icon6)

        self.gridLayout_7.addWidget(self.pushButton_21, 1, 2, 1, 1)

        self.pushButton_22 = QPushButton(self.runswat)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setMinimumSize(QSize(150, 30))
        self.pushButton_22.setFont(font)
        self.pushButton_22.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_22.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/icons/cil-find-in-page.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_22.setIcon(icon7)

        self.gridLayout_7.addWidget(self.pushButton_22, 1, 0, 1, 2)

        self.stackedWidget.addWidget(self.runswat)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.horizontalLayout_9 = QHBoxLayout(self.new_page)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame = QFrame(self.new_page)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.labelBoxBlenderInstalation_56 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_56.setObjectName(u"labelBoxBlenderInstalation_56")
        self.labelBoxBlenderInstalation_56.setFont(font)
        self.labelBoxBlenderInstalation_56.setStyleSheet(u"")

        self.horizontalLayout_11.addWidget(self.labelBoxBlenderInstalation_56)

        self.pushButton_save = QPushButton(self.frame)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMinimumSize(QSize(150, 30))
        self.pushButton_save.setFont(font)
        self.pushButton_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_save.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton_save.setIcon(icon5)

        self.horizontalLayout_11.addWidget(self.pushButton_save)


        self.gridLayout_3.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.comboBox_01 = QComboBox(self.frame)
        self.comboBox_01.addItem("")
        self.comboBox_01.addItem("")
        self.comboBox_01.addItem("")
        self.comboBox_01.addItem("")
        self.comboBox_01.addItem("")
        self.comboBox_01.addItem("")
        self.comboBox_01.setObjectName(u"comboBox_01")
        self.comboBox_01.setFont(font)
        self.comboBox_01.setAutoFillBackground(False)
        self.comboBox_01.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.comboBox_01.setIconSize(QSize(16, 16))
        self.comboBox_01.setFrame(True)

        self.horizontalLayout_12.addWidget(self.comboBox_01)

        self.comboBox_02 = QComboBox(self.frame)
        self.comboBox_02.addItem("")
        self.comboBox_02.addItem("")
        self.comboBox_02.setObjectName(u"comboBox_02")
        self.comboBox_02.setFont(font)
        self.comboBox_02.setAutoFillBackground(False)
        self.comboBox_02.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.comboBox_02.setIconSize(QSize(16, 16))
        self.comboBox_02.setFrame(True)

        self.horizontalLayout_12.addWidget(self.comboBox_02)

        self.comboBox_03 = QComboBox(self.frame)
        self.comboBox_03.addItem("")
        self.comboBox_03.addItem("")
        self.comboBox_03.addItem("")
        self.comboBox_03.setObjectName(u"comboBox_03")
        self.comboBox_03.setFont(font)
        self.comboBox_03.setAutoFillBackground(False)
        self.comboBox_03.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.comboBox_03.setIconSize(QSize(16, 16))
        self.comboBox_03.setFrame(True)

        self.horizontalLayout_12.addWidget(self.comboBox_03)


        self.gridLayout_3.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)

        self.labelBoxBlenderInstalation_53 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_53.setObjectName(u"labelBoxBlenderInstalation_53")
        self.labelBoxBlenderInstalation_53.setFont(font)
        self.labelBoxBlenderInstalation_53.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.labelBoxBlenderInstalation_53, 2, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.radioButton_01 = QRadioButton(self.frame)
        self.radioButton_01.setObjectName(u"radioButton_01")
        self.radioButton_01.setStyleSheet(u"")

        self.horizontalLayout_14.addWidget(self.radioButton_01)

        self.radioButton_02 = QRadioButton(self.frame)
        self.radioButton_02.setObjectName(u"radioButton_02")
        self.radioButton_02.setStyleSheet(u"")

        self.horizontalLayout_14.addWidget(self.radioButton_02)

        self.radioButton_03 = QRadioButton(self.frame)
        self.radioButton_03.setObjectName(u"radioButton_03")
        self.radioButton_03.setStyleSheet(u"")

        self.horizontalLayout_14.addWidget(self.radioButton_03)

        self.radioButton_04 = QRadioButton(self.frame)
        self.radioButton_04.setObjectName(u"radioButton_04")
        self.radioButton_04.setStyleSheet(u"")

        self.horizontalLayout_14.addWidget(self.radioButton_04)


        self.gridLayout_3.addLayout(self.horizontalLayout_14, 3, 0, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.labelBoxBlenderInstalation_52 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_52.setObjectName(u"labelBoxBlenderInstalation_52")
        self.labelBoxBlenderInstalation_52.setFont(font)
        self.labelBoxBlenderInstalation_52.setStyleSheet(u"")

        self.horizontalLayout_15.addWidget(self.labelBoxBlenderInstalation_52)

        self.labelBoxBlenderInstalation_45 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_45.setObjectName(u"labelBoxBlenderInstalation_45")
        self.labelBoxBlenderInstalation_45.setFont(font)
        self.labelBoxBlenderInstalation_45.setStyleSheet(u"")

        self.horizontalLayout_15.addWidget(self.labelBoxBlenderInstalation_45)

        self.labelBoxBlenderInstalation_46 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_46.setObjectName(u"labelBoxBlenderInstalation_46")
        self.labelBoxBlenderInstalation_46.setFont(font)
        self.labelBoxBlenderInstalation_46.setStyleSheet(u"")

        self.horizontalLayout_15.addWidget(self.labelBoxBlenderInstalation_46)


        self.gridLayout_3.addLayout(self.horizontalLayout_15, 4, 0, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.lineEdit_s01 = QLineEdit(self.frame)
        self.lineEdit_s01.setObjectName(u"lineEdit_s01")
        self.lineEdit_s01.setMinimumSize(QSize(0, 30))
        self.lineEdit_s01.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_16.addWidget(self.lineEdit_s01)

        self.lineEdit_s02 = QLineEdit(self.frame)
        self.lineEdit_s02.setObjectName(u"lineEdit_s02")
        self.lineEdit_s02.setMinimumSize(QSize(0, 30))
        self.lineEdit_s02.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_16.addWidget(self.lineEdit_s02)

        self.lineEdit_s03 = QLineEdit(self.frame)
        self.lineEdit_s03.setObjectName(u"lineEdit_s03")
        self.lineEdit_s03.setMinimumSize(QSize(0, 30))
        self.lineEdit_s03.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_16.addWidget(self.lineEdit_s03)


        self.gridLayout_3.addLayout(self.horizontalLayout_16, 5, 0, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.labelBoxBlenderInstalation_54 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_54.setObjectName(u"labelBoxBlenderInstalation_54")
        self.labelBoxBlenderInstalation_54.setFont(font)
        self.labelBoxBlenderInstalation_54.setStyleSheet(u"")

        self.horizontalLayout_17.addWidget(self.labelBoxBlenderInstalation_54)

        self.labelBoxBlenderInstalation_49 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_49.setObjectName(u"labelBoxBlenderInstalation_49")
        self.labelBoxBlenderInstalation_49.setFont(font)
        self.labelBoxBlenderInstalation_49.setStyleSheet(u"")

        self.horizontalLayout_17.addWidget(self.labelBoxBlenderInstalation_49)


        self.gridLayout_3.addLayout(self.horizontalLayout_17, 6, 0, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.lineEdit_s04 = QLineEdit(self.frame)
        self.lineEdit_s04.setObjectName(u"lineEdit_s04")
        self.lineEdit_s04.setMinimumSize(QSize(0, 30))
        self.lineEdit_s04.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_18.addWidget(self.lineEdit_s04)

        self.lineEdit_s05 = QLineEdit(self.frame)
        self.lineEdit_s05.setObjectName(u"lineEdit_s05")
        self.lineEdit_s05.setMinimumSize(QSize(0, 30))
        self.lineEdit_s05.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_18.addWidget(self.lineEdit_s05)


        self.gridLayout_3.addLayout(self.horizontalLayout_18, 7, 0, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.labelBoxBlenderInstalation_48 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_48.setObjectName(u"labelBoxBlenderInstalation_48")
        self.labelBoxBlenderInstalation_48.setFont(font)
        self.labelBoxBlenderInstalation_48.setStyleSheet(u"")

        self.horizontalLayout_19.addWidget(self.labelBoxBlenderInstalation_48)

        self.labelBoxBlenderInstalation_50 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_50.setObjectName(u"labelBoxBlenderInstalation_50")
        self.labelBoxBlenderInstalation_50.setFont(font)
        self.labelBoxBlenderInstalation_50.setStyleSheet(u"")

        self.horizontalLayout_19.addWidget(self.labelBoxBlenderInstalation_50)


        self.gridLayout_3.addLayout(self.horizontalLayout_19, 8, 0, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.lineEdit_s06 = QLineEdit(self.frame)
        self.lineEdit_s06.setObjectName(u"lineEdit_s06")
        self.lineEdit_s06.setMinimumSize(QSize(0, 30))
        self.lineEdit_s06.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_20.addWidget(self.lineEdit_s06)

        self.lineEdit_s07 = QLineEdit(self.frame)
        self.lineEdit_s07.setObjectName(u"lineEdit_s07")
        self.lineEdit_s07.setMinimumSize(QSize(0, 30))
        self.lineEdit_s07.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_20.addWidget(self.lineEdit_s07)


        self.gridLayout_3.addLayout(self.horizontalLayout_20, 9, 0, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.labelBoxBlenderInstalation_51 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_51.setObjectName(u"labelBoxBlenderInstalation_51")
        self.labelBoxBlenderInstalation_51.setFont(font)
        self.labelBoxBlenderInstalation_51.setStyleSheet(u"")

        self.horizontalLayout_21.addWidget(self.labelBoxBlenderInstalation_51)

        self.labelBoxBlenderInstalation_55 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_55.setObjectName(u"labelBoxBlenderInstalation_55")
        self.labelBoxBlenderInstalation_55.setFont(font)
        self.labelBoxBlenderInstalation_55.setStyleSheet(u"")

        self.horizontalLayout_21.addWidget(self.labelBoxBlenderInstalation_55)


        self.gridLayout_3.addLayout(self.horizontalLayout_21, 10, 0, 1, 1)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.lineEdit_s08 = QLineEdit(self.frame)
        self.lineEdit_s08.setObjectName(u"lineEdit_s08")
        self.lineEdit_s08.setMinimumSize(QSize(0, 30))
        self.lineEdit_s08.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_22.addWidget(self.lineEdit_s08)

        self.lineEdit_s09 = QLineEdit(self.frame)
        self.lineEdit_s09.setObjectName(u"lineEdit_s09")
        self.lineEdit_s09.setMinimumSize(QSize(0, 30))
        self.lineEdit_s09.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_22.addWidget(self.lineEdit_s09)


        self.gridLayout_3.addLayout(self.horizontalLayout_22, 11, 0, 1, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.labelBoxBlenderInstalation_61 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_61.setObjectName(u"labelBoxBlenderInstalation_61")
        self.labelBoxBlenderInstalation_61.setFont(font)
        self.labelBoxBlenderInstalation_61.setStyleSheet(u"")

        self.horizontalLayout_23.addWidget(self.labelBoxBlenderInstalation_61)

        self.labelBoxBlenderInstalation_62 = QLabel(self.frame)
        self.labelBoxBlenderInstalation_62.setObjectName(u"labelBoxBlenderInstalation_62")
        self.labelBoxBlenderInstalation_62.setFont(font)
        self.labelBoxBlenderInstalation_62.setStyleSheet(u"")

        self.horizontalLayout_23.addWidget(self.labelBoxBlenderInstalation_62)


        self.gridLayout_3.addLayout(self.horizontalLayout_23, 12, 0, 1, 1)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.lineEdit_s10 = QLineEdit(self.frame)
        self.lineEdit_s10.setObjectName(u"lineEdit_s10")
        self.lineEdit_s10.setMinimumSize(QSize(0, 30))
        self.lineEdit_s10.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_24.addWidget(self.lineEdit_s10)

        self.lineEdit_s11 = QLineEdit(self.frame)
        self.lineEdit_s11.setObjectName(u"lineEdit_s11")
        self.lineEdit_s11.setMinimumSize(QSize(0, 30))
        self.lineEdit_s11.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_24.addWidget(self.lineEdit_s11)


        self.gridLayout_3.addLayout(self.horizontalLayout_24, 13, 0, 1, 1)


        self.horizontalLayout_9.addWidget(self.frame)
        # self.verticalLayout_20 = QVBoxLayout(self.new_page)
        # self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        # self.pushButton_2 = QPushButton(self.new_page)
        # self.pushButton_2.setObjectName(u"pushButton_2")
        # self.pushButton_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        # self.verticalLayout_20.addWidget(self.pushButton_2)

        # self.pushButton_3 = QPushButton(self.new_page)
        # self.pushButton_3.setObjectName(u"pushButton_3")
        # self.pushButton_3.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        # self.verticalLayout_20.addWidget(self.pushButton_3)

        # self.pushButton_4 = QPushButton(self.new_page)
        # self.pushButton_4.setObjectName(u"pushButton_4")
        # self.pushButton_4.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        # self.verticalLayout_20.addWidget(self.pushButton_4)

        # self.label = QLabel(self.new_page)
        # self.label.setObjectName(u"label")
        # self.label.setAlignment(Qt.AlignCenter)

        # self.verticalLayout_20.addWidget(self.label)

        self.stackedWidget.addWidget(self.new_page)
        self.computer_info = QWidget()
        self.computer_info.setObjectName(u"computer_info")
        self.verticalLayout_22 = QVBoxLayout(self.computer_info)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.graphicsView = QChartView(self.computer_info)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_21.addWidget(self.graphicsView)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.computer_info_start = QPushButton(self.computer_info)
        self.computer_info_start.setObjectName(u"computer_info_start")
        self.computer_info_start.setLayoutDirection(Qt.LeftToRight)
        self.computer_info_start.setAutoFillBackground(False)
        self.computer_info_start.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_6.addWidget(self.computer_info_start)

        self.computer_info_clear = QPushButton(self.computer_info)
        self.computer_info_clear.setObjectName(u"computer_info_clear")
        self.computer_info_clear.setLayoutDirection(Qt.LeftToRight)
        self.computer_info_clear.setAutoFillBackground(False)
        self.computer_info_clear.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_6.addWidget(self.computer_info_clear)


        self.verticalLayout_21.addLayout(self.horizontalLayout_6)


        self.verticalLayout_22.addLayout(self.verticalLayout_21)

        self.stackedWidget.addWidget(self.computer_info)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_theme = QPushButton(self.topMenus)
        self.btn_theme.setObjectName(u"btn_theme")
        sizePolicy.setHeightForWidth(self.btn_theme.sizePolicy().hasHeightForWidth())
        self.btn_theme.setSizePolicy(sizePolicy)
        self.btn_theme.setMinimumSize(QSize(0, 45))
        self.btn_theme.setFont(font)
        self.btn_theme.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_theme.setLayoutDirection(Qt.LeftToRight)
        self.btn_theme.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-3d.png);")

        self.verticalLayout_14.addWidget(self.btn_theme)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"SWAT-APWF", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Module SCS", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"Input File", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.btn_swat.setText(QCoreApplication.translate("MainWindow", u"Run SWAT", None))
        self.btn_computer.setText(QCoreApplication.translate("MainWindow", u"Performance", None))
        # self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Tool Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.btn_adjustments.setText(QCoreApplication.translate("MainWindow", u"Adjustments", None))
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">PyDracula</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">An interface created using Python and PySide (support for PyQt), and with colors based on the Dracula theme created by Zen"
                        "o Rocha.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\"></span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: UCAS Xianfeng Song team</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert UI</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-uic main.ui &gt; ui_main.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert QRC</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u5177\u767e\u5b9d\u7bb1", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.btn_theme.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.pushButton_01.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_21.setText(QCoreApplication.translate("MainWindow", u"RUN SWAT", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"Check Input", None))
        self.labelBoxBlenderInstalation_1.setText(QCoreApplication.translate("MainWindow", u"TxtInOut file generated by Arcswat*", None))
        self.lineEdit_01.setText("")
        self.lineEdit_01.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_02.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_2.setText(QCoreApplication.translate("MainWindow", u"Configuration file path for the parameter template*", None))
        self.lineEdit_02.setText("")
        self.lineEdit_02.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_04.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_03.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_4.setText(QCoreApplication.translate("MainWindow", u"Evapotranspiration observation file", None))
        self.lineEdit_04.setText("")
        self.lineEdit_04.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_3.setText(QCoreApplication.translate("MainWindow", u"Flow observation data", None))
        self.lineEdit_03.setText("")
        self.lineEdit_03.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_06.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_05.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_6.setText(QCoreApplication.translate("MainWindow", u"Observation files used for ETC analysis", None))
        self.lineEdit_06.setText("")
        self.lineEdit_06.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_5.setText(QCoreApplication.translate("MainWindow", u"Soil moisture observation file", None))
        self.lineEdit_05.setText("")
        self.lineEdit_05.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_08.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_07.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_8.setText(QCoreApplication.translate("MainWindow", u"Latin Hypercube Sampling results*", None))
        self.lineEdit_08.setText("")
        self.lineEdit_08.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_7.setText(QCoreApplication.translate("MainWindow", u"SWAT simulation output path*", None))
        self.lineEdit_07.setText("")
        self.lineEdit_07.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_10.setText("")
        self.lineEdit_10.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_12.setText("")
        self.lineEdit_12.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_10.setText(QCoreApplication.translate("MainWindow", u"Temporary working directory for multi-threading*", None))
        self.labelBoxBlenderInstalation_11.setText(QCoreApplication.translate("MainWindow", u"Parameter iteration weight configuration file*", None))
        self.pushButton_09.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.lineEdit_09.setText("")
        self.lineEdit_09.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_11.setText("")
        self.lineEdit_11.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_12.setText(QCoreApplication.translate("MainWindow", u"Image storage location*", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelBoxBlenderInstalation_9.setText(QCoreApplication.translate("MainWindow", u"Suggested parameter template configuration file*", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.labelBoxBlenderInstalation_56.setText(QCoreApplication.translate("MainWindow", u"Debug type", None))
        self.pushButton_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.comboBox_01.setItemText(0, QCoreApplication.translate("MainWindow", u"flow", None))
        self.comboBox_01.setItemText(1, QCoreApplication.translate("MainWindow", u"ET", None))
        self.comboBox_01.setItemText(2, QCoreApplication.translate("MainWindow", u"SW", None))
        self.comboBox_01.setItemText(3, QCoreApplication.translate("MainWindow", u"flow&ET", None))
        self.comboBox_01.setItemText(4, QCoreApplication.translate("MainWindow", u"flow&SW", None))
        self.comboBox_01.setItemText(5, QCoreApplication.translate("MainWindow", u"TC", None))

        self.comboBox_02.setItemText(0, QCoreApplication.translate("MainWindow", u"SUB", None))
        self.comboBox_02.setItemText(1, QCoreApplication.translate("MainWindow", u"HRU", None))

        self.comboBox_03.setItemText(0, QCoreApplication.translate("MainWindow", u"Mon", None))
        self.comboBox_03.setItemText(1, QCoreApplication.translate("MainWindow", u"8days", None))
        self.comboBox_03.setItemText(2, QCoreApplication.translate("MainWindow", u"days", None))

        self.labelBoxBlenderInstalation_53.setText(QCoreApplication.translate("MainWindow", u"Evaluation value", None))
        self.radioButton_01.setText(QCoreApplication.translate("MainWindow", u"R2", None))
        self.radioButton_02.setText(QCoreApplication.translate("MainWindow", u"Nes", None))
        self.radioButton_03.setText(QCoreApplication.translate("MainWindow", u"PBIAS", None))
        self.radioButton_04.setText(QCoreApplication.translate("MainWindow", u"KGE", None))
        self.labelBoxBlenderInstalation_52.setText(QCoreApplication.translate("MainWindow", u"Number of simulations", None))
        self.labelBoxBlenderInstalation_45.setText(QCoreApplication.translate("MainWindow", u"Parallel processing cores", None))
        self.labelBoxBlenderInstalation_46.setText(QCoreApplication.translate("MainWindow", u"Number of iterations", None))
        self.lineEdit_s01.setText("")
        self.lineEdit_s01.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s02.setText("")
        self.lineEdit_s02.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s03.setText("")
        self.lineEdit_s03.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_54.setText(QCoreApplication.translate("MainWindow", u"Select SUB", None))
        self.labelBoxBlenderInstalation_49.setText(QCoreApplication.translate("MainWindow", u"Select HRU", None))
        self.lineEdit_s04.setText("")
        self.lineEdit_s04.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s05.setText("")
        self.lineEdit_s05.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_48.setText(QCoreApplication.translate("MainWindow", u"Select RCH", None))
        self.labelBoxBlenderInstalation_50.setText(QCoreApplication.translate("MainWindow", u"Weight", None))
        self.lineEdit_s06.setText("")
        self.lineEdit_s06.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s07.setText("")
        self.lineEdit_s07.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_51.setText(QCoreApplication.translate("MainWindow", u"Data start period", None))
        self.labelBoxBlenderInstalation_55.setText(QCoreApplication.translate("MainWindow", u"Data end period", None))
        self.lineEdit_s08.setText("")
        self.lineEdit_s08.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s09.setText("")
        self.lineEdit_s09.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.labelBoxBlenderInstalation_61.setText(QCoreApplication.translate("MainWindow", u"Simulation start time period", None))
        self.labelBoxBlenderInstalation_62.setText(QCoreApplication.translate("MainWindow", u"Simulation end time period", None))
        self.lineEdit_s10.setText("")
        self.lineEdit_s10.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.lineEdit_s11.setText("")
        self.lineEdit_s11.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        # self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u8bf4\u660e\u4e66", None))
        # self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u7f51\u5740", None))
        # self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u5207\u6362\u56fe\u7247", None))
        # self.label.setText(QCoreApplication.translate("MainWindow", u"NEW PAGE TEST", None))
        self.computer_info_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.computer_info_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.btn_theme.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: UCAS Song Xianfeng team", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi


