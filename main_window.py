# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 604)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 501, 561))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(520, 30, 311, 541))
        self.textBrowser.setObjectName("textBrowser")
        self.is_block_short_key = QtWidgets.QCheckBox(self.centralwidget)
        self.is_block_short_key.setGeometry(QtCore.QRect(510, 0, 111, 19))
        self.is_block_short_key.setObjectName("is_block_short_key")
        self.start_all = QtWidgets.QPushButton(self.centralwidget)
        self.start_all.setGeometry(QtCore.QRect(630, 0, 101, 23))
        self.start_all.setObjectName("start_all")
        self.stop_all = QtWidgets.QPushButton(self.centralwidget)
        self.stop_all.setGeometry(QtCore.QRect(740, 0, 91, 23))
        self.stop_all.setObjectName("stop_all")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_5 = QtWidgets.QMenu(self.menu_3)
        self.menu_5.setObjectName("menu_5")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menuyinpin = QtWidgets.QMenu(self.menu_6)
        self.menuyinpin.setObjectName("menuyinpin")
        MainWindow.setMenuBar(self.menubar)
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionimport = QtWidgets.QAction(MainWindow)
        self.actionimport.setObjectName("actionimport")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionadd_preset = QtWidgets.QAction(MainWindow)
        self.actionadd_preset.setObjectName("actionadd_preset")
        self.actionadd_control = QtWidgets.QAction(MainWindow)
        self.actionadd_control.setObjectName("actionadd_control")
        self.action_optop = QtWidgets.QAction(MainWindow)
        self.action_optop.setObjectName("action_optop")
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        self.actionhelp = QtWidgets.QAction(MainWindow)
        self.actionhelp.setObjectName("actionhelp")
        self.action_to_night_2 = QtWidgets.QAction(MainWindow)
        self.action_to_night_2.setObjectName("action_to_night_2")
        self.action_to_night = QtWidgets.QAction(MainWindow)
        self.action_to_night.setObjectName("action_to_night")
        self.action_to_early = QtWidgets.QAction(MainWindow)
        self.action_to_early.setObjectName("action_to_early")
        self.action_to_by_win = QtWidgets.QAction(MainWindow)
        self.action_to_by_win.setObjectName("action_to_by_win")
        self.actionyinpin_start = QtWidgets.QAction(MainWindow)
        self.actionyinpin_start.setObjectName("actionyinpin_start")
        self.actionyinpin_stop = QtWidgets.QAction(MainWindow)
        self.actionyinpin_stop.setObjectName("actionyinpin_stop")
        self.actionsetting = QtWidgets.QAction(MainWindow)
        self.actionsetting.setObjectName("actionsetting")
        self.menu.addAction(self.actionsave)
        self.menu.addAction(self.actionimport)
        self.menu.addAction(self.actionexit)
        self.menu_2.addAction(self.actionadd_preset)
        self.menu_2.addAction(self.actionadd_control)
        self.menu_5.addAction(self.action_to_night_2)
        self.menu_5.addAction(self.action_to_early)
        self.menu_3.addAction(self.action_optop)
        self.menu_3.addAction(self.menu_5.menuAction())
        self.menu_3.addAction(self.action_to_by_win)
        self.menu_4.addAction(self.actionabout)
        self.menu_4.addAction(self.actionhelp)
        self.menuyinpin.addAction(self.actionyinpin_start)
        self.menuyinpin.addAction(self.actionyinpin_stop)
        self.menu_6.addAction(self.menuyinpin.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.is_block_short_key.setToolTip(_translate("MainWindow", "暂时屏蔽快捷键以便进行生成区域选定，创建多个AI导出文档"))
        self.is_block_short_key.setText(_translate("MainWindow", "暂时屏蔽快捷键"))
        self.start_all.setToolTip(_translate("MainWindow", "对当前所有任务进行顺序流水线执行"))
        self.start_all.setText(_translate("MainWindow", "开始批量操作"))
        self.stop_all.setToolTip(_translate("MainWindow", "执行流水线任务操作后，按此键可一键中止"))
        self.stop_all.setText(_translate("MainWindow", "中止所有操作"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "添加"))
        self.menu_3.setTitle(_translate("MainWindow", "显示"))
        self.menu_5.setTitle(_translate("MainWindow", "切换昼夜模式"))
        self.menu_4.setTitle(_translate("MainWindow", "关于与帮助"))
        self.menu_6.setTitle(_translate("MainWindow", "设置"))
        self.menuyinpin.setTitle(_translate("MainWindow", "任务结束后是否播放音频音频"))
        self.actionsave.setText(_translate("MainWindow", "保存工程 （将当前所有工程保存为工程文件） <Ctrl+S>"))
        self.actionsave.setIconText(_translate("MainWindow", "导出工程"))
        self.actionimport.setText(_translate("MainWindow", "读取工程 （在本工程的基础上增加工程文件） <Ctrl+R>"))
        self.actionimport.setIconText(_translate("MainWindow", "导入工程"))
        self.actionexit.setText(_translate("MainWindow", "退出 <Ctrl+Q>"))
        self.actionexit.setIconText(_translate("MainWindow", "退出"))
        self.actionadd_preset.setText(_translate("MainWindow", "添加新预设"))
        self.actionadd_control.setText(_translate("MainWindow", "添加controlnet"))
        self.action_optop.setText(_translate("MainWindow", "切换置顶状态"))
        self.actionabout.setText(_translate("MainWindow", "关于Psdlink pro"))
        self.actionhelp.setText(_translate("MainWindow", "帮助"))
        self.action_to_night_2.setText(_translate("MainWindow", "夜间模式"))
        self.action_to_night.setText(_translate("MainWindow", "夜间模式"))
        self.action_to_early.setText(_translate("MainWindow", "昼间模式"))
        self.action_to_by_win.setText(_translate("MainWindow", "切换到ps插件界面"))
        self.action_to_by_win.setToolTip(_translate("MainWindow", "切换到ps插件界面"))
        self.actionyinpin_start.setText(_translate("MainWindow", "音频开启"))
        self.actionyinpin_stop.setText(_translate("MainWindow", "音频关闭"))
        self.actionsetting.setText(_translate("MainWindow", "Autodl账号密码配置"))