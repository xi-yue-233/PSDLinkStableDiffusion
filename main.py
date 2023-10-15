# designer设计，加载ui运行
import threading

import keyboard
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator, QTextCharFormat, QColor, \
    QMouseEvent, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QWidget, QToolBar, QAction, QLayout, \
    QShortcut, QDesktopWidget
from PyQt5.QtCore import Qt, QRegularExpression, QPoint, QCoreApplication

from PyQt5 import QtWidgets

import main_window
import null_tab
import small_tab
import small_window
import tab_window
from add_preset_win import add_preset_win, add_cn_preset_win
from button_mehod import *
from playsound import check_is_sound, repair_is_sound
from ps_tools import auto_doc_name
from save_import_project import save_project, import_project, save_project_self
from set_cn_preset import set_cn_win
from setting_preset import open_set_preset
from tool_bar_method import *

# 记录tabs
from update_combo import update_preset, upadate_cn_preset

application_list = []
application_small_list = []
index = 0
is_block=False
ispswindow=False

# PS插件窗口
class small_windows(QMainWindow):
    __start_pos = None
    __end_pos = None
    __is_tracking = False

    def __init__(self, parent):
        super().__init__()
        sys.excepthook = exceptOutConfig
        self.parent = parent
        self.ui_null_tab = null_tab.Ui_Form()
        self.null_tab_windows = QtWidgets.QWidget()
        self.ui = small_window.Ui_MainWindow()
        self.ui.setupUi(self)
        set_opacity(self)
        self.setWindowFlags(parent.windowFlags() | Qt.FramelessWindowHint)
        parent.hide()
        self.show()

        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten_erro)

        self.ui.textBrowser.clear()
        self.ui.textBrowser.insertHtml(parent.ui.textBrowser.toHtml())

        self.small_tool_bar(parent)
        self.init_tab(parent)
        self.setStyleSheet("QToolTip { color: blue; background: black }")

        self.ui.tabWidget: QTabWidget
        # 绑定关闭标签子页
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.ui.tabWidget.currentChanged.connect(
            lambda: parent.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.currentIndex()))

        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            self.move(data["save_x"],data["save_y"])

    def change_to_Main_w(self, parent):
        repair_pswindow(False)
        parent.show()
        parent.ui.textBrowser.clear()
        parent.ui.textBrowser.insertHtml(self.ui.textBrowser.toHtml())
        sys.stdout = EmittingStr(textWritten=parent.outputWritten)
        sys.stderr = EmittingStr(textWritten=parent.outputWritten_erro)
        set_opacity(parent)
        self.hide()

    def mouseMoveEvent(self, event_: QMouseEvent):
        if self.__is_tracking == True:
            self.__end_pos = event_.pos() - self.__start_pos
            self.move(self.pos() + self.__end_pos)

    def mousePressEvent(self, event_: QMouseEvent):
        if event_.button() == Qt.LeftButton:
            self.__is_tracking = True
            self.__start_pos = QPoint(event_.x(), event_.y())

    def mouseReleaseEvent(self, event_: QMouseEvent):
        if event_.button() == Qt.LeftButton:
            self.__is_tracking = False
            self.__start_pos = None
            self.__end_pos = None

            screen = QDesktopWidget().screenGeometry()
            limx = screen.width() - self.geometry().width()
            limy = screen.height() - self.geometry().height()
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            save_x = self.geometry().x()
            if save_x > limx:
                save_x = limx
            elif save_x < 0:
                save_x = 0
            save_y = self.geometry().y()
            if save_y > limy:
                save_y = limy
            elif save_y < 0:
                save_y = 0
            with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                data = json.load(f)
                data["save_x"] = save_x
                data["save_y"] = save_y
            with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)

    def outputWritten(self, text):
        format = QTextCharFormat()
        format.setForeground(QColor(85, 130, 66))
        self.ui.textBrowser.setCurrentCharFormat(format)
        self.ui.textBrowser.insertPlainText(text)
        self.ui.textBrowser.ensureCursorVisible()

    def outputWritten_erro(self, text):
        format = QTextCharFormat()
        format.setForeground(QColor(211, 38, 38))
        self.ui.textBrowser.setCurrentCharFormat(format)
        self.ui.textBrowser.insertPlainText(text)
        self.ui.textBrowser.ensureCursorVisible()

    def close_tab(self, n):
        # 删除tab
        global index
        index = index - 1
        self.ui.tabWidget.removeTab(n)
        self.ui.tabWidget.setCurrentIndex(n - 1)
        self.parent.ui.tabWidget.removeTab(n)
        self.parent.ui.tabWidget.setCurrentIndex(n - 1)
        # 把当前的tab从application_list删除
        application_list.pop()

    def add_tab(self):
        global index
        self.parent.add_tab()
        self.trans_main_to_small(self.parent)
        self.ui.tabWidget.setCurrentIndex(index - 1)

    def init_tab(self, parent):
        """
        初始化，通过designer设计，会初始有两个标签子页，需要先去除，然后添加一个标签子页，并将其设置为按钮添加，点击可以添加子页
        """
        self.ui.tabWidget: QTabWidget
        # 关闭所有标签子页
        self.ui.tabWidget.clear()
        # 添加一个标签子页，没有文本，索引为0
        self.ui_null_tab.setupUi(self.null_tab_windows)
        self.ui.tabWidget.addTab(self.null_tab_windows, "")
        # 对索引为0的该标签子页设置按钮
        btn = QPushButton("+")
        self.ui.tabWidget.tabBar().setTabButton(0, self.ui.tabWidget.tabBar().RightSide, btn)
        #
        btn.clicked.connect(self.add_tab)
        if len(application_list) > 0:
            self.trans_main_to_small(parent)
        else:
            self.ui.tabWidget.setCurrentIndex(0)

    def trans_main_to_small(self, parent):
        # 转化主页面的元素为小窗口元素
        # self.ui.tabWidget.clear()
        self.index = 0
        while self.ui.tabWidget.count() > 1:
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.currentIndex() - 1)
            self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex())
        application_small_list.clear()
        for i in application_list:
            self.index = self.index + 1
            self.tab_w = QtWidgets.QWidget()
            self.ui_tab_w = small_tab.Ui_Form()
            self.ui_tab_w.setupUi(self.tab_w)
            # 连接tab上的元素
            # self.tabs_bind()
            self.ui_tab_w.layer_name.setText(i.layer_name.text())
            for j in range(i.preset_combo.count()):
                self.ui_tab_w.preset_combo.addItem(i.preset_combo.itemText(j))
            self.ui_tab_w.preset_combo.setCurrentIndex(i.preset_combo.currentIndex())
            self.ui_tab_w.add_positive_edit.setText(i.add_positive_edit.text())
            self.ui_tab_w.add_negative_edit.setText(i.add_negative_edit.text())
            self.ui_tab_w.is_use_translate.setChecked(i.is_use_translate.isChecked())
            self.ui_tab_w.paint_weight.setText(i.paint_weight.text())
            self.ui_tab_w.paint_count.setText(i.paint_count.text())
            self.ui_tab_w.webui_url.setText(i.webui_url.text())
            self.ui_tab_w.is_hd.setChecked(i.is_hd.isChecked())
            self.ui_tab_w.hd_weight.setText(i.hd_weight.text())
            for j in range(i.cn0_preset.count()):
                self.ui_tab_w.cn0_preset.addItem(i.cn0_preset.itemText(j))
            self.ui_tab_w.cn0_preset.setCurrentIndex(i.cn0_preset.currentIndex())
            self.ui_tab_w.lama_url.setText(i.lama_url.text())

            # # 控制重绘幅度和张数的输入范围
            self.ui_tab_w.paint_count.setValidator(QIntValidator(1, 9999999))
            self.reg = QRegularExpression('^0\.(0[1-9]|[1-9]\d?)$|^1\.00$')
            self.validator = QRegularExpressionValidator()
            self.validator.setRegularExpression(self.reg)
            self.ui_tab_w.paint_weight.setValidator(self.validator)
            self.ui_tab_w.hd_weight.setValidator(self.validator)

            self.ui_tab_w.layer_name.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].layer_name.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].layer_name.text()))
            self.ui_tab_w.preset_combo.currentIndexChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].preset_combo.setCurrentIndex(
                    application_small_list[self.ui.tabWidget.currentIndex()].preset_combo.currentIndex()))
            self.ui_tab_w.add_positive_edit.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].add_positive_edit.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].add_positive_edit.text()))
            self.ui_tab_w.add_negative_edit.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].add_negative_edit.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].add_negative_edit.text()))
            self.ui_tab_w.is_use_translate.stateChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].is_use_translate.setChecked(
                    application_small_list[self.ui.tabWidget.currentIndex()].is_use_translate.isChecked()))
            self.ui_tab_w.paint_weight.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].paint_weight.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].paint_weight.text()))
            self.ui_tab_w.paint_count.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].paint_count.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].paint_count.text()))
            self.ui_tab_w.webui_url.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].webui_url.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].webui_url.text()))
            self.ui_tab_w.is_hd.stateChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].is_hd.setChecked(
                    application_small_list[self.ui.tabWidget.currentIndex()].is_hd.isChecked()))
            self.ui_tab_w.hd_weight.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].hd_weight.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].hd_weight.text()))
            self.ui_tab_w.cn0_preset.currentIndexChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].cn0_preset.setCurrentIndex(
                    application_small_list[self.ui.tabWidget.currentIndex()].cn0_preset.currentIndex()))
            self.ui_tab_w.lama_url.textChanged.connect(
                lambda: application_list[self.ui.tabWidget.currentIndex()].lama_url.setText(
                    application_small_list[self.ui.tabWidget.currentIndex()].lama_url.text()))

            # 连接tab上的预设设置按钮
            self.ui_tab_w.set_preset.clicked.connect(
                lambda: open_set_preset(self.parent, application_small_list[
                    self.ui.tabWidget.currentIndex()].preset_combo.currentIndex(), application_list,
                                        application_small_list))

            # 连接设置预设按钮
            self.ui_tab_w.cn0_preset_set_btn.clicked.connect(
                lambda: set_cn_win(self.parent,
                                   application_small_list[self.ui.tabWidget.currentIndex()].cn0_preset.currentIndex(),
                                   application_list, application_small_list))

            # 自动匹配文件名
            self.ui_tab_w.auto_layer_name.clicked.connect(
                lambda: auto_doc_name(application_list, application_small_list))
            # 全应用该url和id
            self.ui_tab_w.all_url_btn.clicked.connect(
                lambda: all_url_method(self.ui.tabWidget.currentIndex(), application_list, application_small_list))
            self.ui_tab_w.all_hd_btn.clicked.connect(
                lambda: all_hd_method(self.ui.tabWidget.currentIndex(), application_list, application_small_list))

            # 运算按钮
            self.ui_tab_w.import_sd_btn.clicked.connect(
                lambda: parent.short_key_import_sd())
            self.ui_tab_w.start_cal_btn.clicked.connect(
                lambda: parent.start_caculate())
            self.ui_tab_w.only_import_btn.clicked.connect(
                lambda: parent.only_import())
            self.ui_tab_w.back_ps_btn.clicked.connect(
                lambda: parent.import_back_ps())
            self.ui_tab_w.hd_btn.clicked.connect(
                lambda: parent.hd_back_ps_btn())
            self.ui_tab_w.lama_import.clicked.connect(
                lambda: parent.Lama_export())
            self.ui_tab_w.lama_export.clicked.connect(
                lambda: parent.Lama_import())

            # 存档
            self.ui_tab_w.export_project_btn.clicked.connect(
                lambda: save_project_self(self, application_list, self.ui.tabWidget.currentIndex()))

            # self.tabs_bind()

            # 插入标签
            self.ui.tabWidget.insertTab(self.ui.tabWidget.count() - 1, self.tab_w, i.tab_name.text())
            application_small_list.append(self.ui_tab_w)
        self.ui.tabWidget.setTabsClosable(True)

        self.ui.tabWidget.setCurrentIndex(parent.ui.tabWidget.currentIndex())

    def small_tool_bar(self, parent):
        self.ui.action_to_main_win.triggered.connect(lambda: self.change_to_Main_w(parent))

        # 绑定工具栏的功能
        self.ui.actionadd_control.triggered.connect(
            lambda: add_cn_preset_win(parent, application_list, application_small_list))
        self.ui.actionadd_preset.triggered.connect(
            lambda: add_preset_win(parent, application_list, application_small_list))
        self.ui.action_optop.triggered.connect(lambda: [toggle_topmost(self), toggle_topmost(parent), parent.hide()])
        self.ui.action_to_night_2.triggered.connect(lambda: repair_is_night(True))
        self.ui.action_to_early.triggered.connect(lambda: repair_is_night(False))
        self.ui.actionopcacity_true.triggered.connect(lambda: repair_is_opacity(True,self))
        self.ui.actionopcacity_false.triggered.connect(lambda: repair_is_opacity(False,self))

        # 绑定副窗口工作栏功能
        # self.ui_small.action_to_main_win.triggered.connect(lambda: self.change_main_window())

        # 绑定开始批量操作
        self.ui.start_all.clicked.connect(lambda: parent.deal_all_method())
        self.ui.stop_all.clicked.connect(lambda: parent.stop_all_method())

        # 设置是否播放声音
        self.ui.actionyinpin_start.triggered.connect(lambda: repair_is_sound(True))
        self.ui.actionyinpin_stop.triggered.connect(lambda: repair_is_sound(False))

        # 存档
        self.ui.actionsave.triggered.connect(lambda: save_project(parent, application_list))
        self.ui.actionimport.triggered.connect(
            lambda: [import_project(parent, application_list), self.trans_main_to_small(parent)])
        self.ui.actionexit.triggered.connect(lambda: self.close())

        shortcut = QShortcut(QKeySequence('Ctrl+s'), self)
        shortcut.activated.connect(lambda: save_project(parent, application_list))
        shortcut1 = QShortcut(QKeySequence('Ctrl+r'), self)
        shortcut1.activated.connect(
            lambda: [import_project(parent, application_list), self.trans_main_to_small(parent)])
        shortcut2 = QShortcut(QKeySequence('Ctrl+q'), self)
        shortcut2.activated.connect(lambda: self.close())

        def check_block():
            global is_block
            is_block = self.ui.is_block_short_key.isChecked()
        self.ui.is_block_short_key.stateChanged.connect(lambda: [check_block(),parent.block_all_short_key()])

    def closeEvent(self, event):
        try:
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                data = json.load(f)
                data["setting_index"] = application_list[0].preset_combo.currentIndex()
                data["am"] = application_list[0].paint_weight.text()
                data["ct"] = application_list[0].paint_count.text()
                data["url"] = application_list[0].webui_url.text()
                data["hd"] = application_list[0].is_hd.isChecked()
                data["hdam"] = application_list[0].hd_weight.text()
                data["control_index"] = application_list[0].cn0_preset.currentIndex()
                data["lama_url"] = application_list[0].lama_url.text()
            with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)
            event.accept()
        except:
            event.accept()

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class Main_windows(QMainWindow):
    __start_pos = None
    __end_pos = None
    __is_tracking = False

    # 记录使用过的标签索引
    def __init__(self):
        super().__init__()
        # 注册主窗口
        self.ui_null_tab = null_tab.Ui_Form()
        self.null_tab_windows = QtWidgets.QWidget()
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        set_opacity(self)

        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten_erro)
        self.setWindowTitle("PSDLink pro")
        self.main_tool_bar()
        self.setStyleSheet("QToolTip { color: blue; background: black }")

        self.init_tab()
        self.ui.tabWidget: QTabWidget
        # 绑定关闭标签子页
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.block_all_short_key()


    def first_boot(self):
        global ispswindow
        if ispswindow:
            self.init_sub_win()

    def mouseMoveEvent(self, event_: QMouseEvent):
        if self.__is_tracking == True:
            self.__end_pos = event_.pos() - self.__start_pos
            self.move(self.pos() + self.__end_pos)

    def mousePressEvent(self, event_: QMouseEvent):
        if event_.button() == Qt.LeftButton:
            self.__is_tracking = True
            self.__start_pos = QPoint(event_.x(), event_.y())

    def mouseReleaseEvent(self, event_: QMouseEvent):
        if event_.button() == Qt.LeftButton:
            self.__is_tracking = False
            self.__start_pos = None
            self.__end_pos = None

    def outputWritten(self, text):
        format = QTextCharFormat()
        format.setForeground(QColor(85, 130, 66))
        self.ui.textBrowser.setCurrentCharFormat(format)
        self.ui.textBrowser.insertPlainText(text)
        self.ui.textBrowser.ensureCursorVisible()

    def outputWritten_erro(self, text):
        format = QTextCharFormat()
        format.setForeground(QColor(211, 38, 38))
        self.ui.textBrowser.setCurrentCharFormat(format)
        self.ui.textBrowser.insertPlainText(text)
        self.ui.textBrowser.ensureCursorVisible()

    def close_tab(self, n):
        # 删除tab
        global index
        index = index - 1
        self.ui.tabWidget.removeTab(n)
        self.ui.tabWidget.setCurrentIndex(n - 1)
        # 把当前的tab从application_list删除
        application_list.pop()

    def add_tab(self, tab=None, tab_w=None):
        # 在次末尾处添加
        global index
        index = index + 1
        # 注册工程窗口
        if tab != None:
            self.ui.tabWidget.insertTab(self.ui.tabWidget.count() -1, tab_w, tab.tab_name.text())
            self.ui.tabWidget.setTabsClosable(True)
            # 把视图指向最新一个tab
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 2)
            print(f"增加新任务 {tab.tab_name.text()}")
        else:
            self.tab_w = QtWidgets.QWidget()
            self.ui_tab_w = tab_window.Ui_Form()
            self.ui_tab_w.setupUi(self.tab_w)
            # 连接tab上的元素
            self.tabs_bind()
            self.ui.tabWidget.insertTab(self.ui.tabWidget.count() -1, self.tab_w, "任务" + str(index))
            self.ui.tabWidget.setTabsClosable(True)
            self.ui_tab_w.tab_name.setText("任务" + str(index))

            # 把视图指向最新一个tab
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 2)
            # 把当前的tab加入application_list
            application_list.append(self.ui_tab_w)
            print(f"增加新任务 任务{index}")
        # print(self.ui.tabWidget.currentIndex())

    def init_tab(self):
        """
        初始化，通过designer设计，会初始有两个标签子页，需要先去除，然后添加一个标签子页，并将其设置为按钮添加，点击可以添加子页 
        """
        self.ui.tabWidget: QTabWidget
        # 关闭所有标签子页
        self.ui.tabWidget.clear()
        # 添加一个标签子页，没有文本，索引为0
        self.ui_null_tab.setupUi(self.null_tab_windows)
        self.ui.tabWidget.addTab(self.null_tab_windows, "")
        # 对索引为0的该标签子页设置按钮
        btn = QPushButton("+")
        self.ui.tabWidget.tabBar().setTabButton(0, self.ui.tabWidget.tabBar().RightSide, btn)
        #
        btn.clicked.connect(lambda: self.add_tab())
        self.add_tab()

    def rename_tab(self, application_list):
        # 重命名标签页
        currentIndex = self.ui.tabWidget.currentIndex()
        self.ui.tabWidget.setTabText(currentIndex, application_list[currentIndex].tab_name.text())

    def deal_all_method(self):
        if running_variable.all_running == False:
            running_variable.all_running = True
            running_variable.running = True
            t = threading.Thread(target=import_to_sd, args=(application_list,))
            t.start()
        else:
            print("当前已经在执行批量任务了")

    def stop_all_method(self):
        running_variable.all_running = False
        running_variable.running = False
        print("中止全部任务")

    # 快捷键导入SD
    def short_key_import_sd(self):
        if running_variable.running == False:
            threads = []
            threads.append(threading.Thread(target=short_key_import_to_sd,
                                            args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 开始运算
    def start_caculate(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=begin_caculate, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 放大
    def hd_back_ps_btn(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=hd_back_ps, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 传回ps
    def import_back_ps(self):
        if running_variable.running == False:
            threads = []
            threads.append(threading.Thread(target=back_ps, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 仅导入
    def only_import(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=only_import, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 仅导入并开始
    def only_import_start(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=only_import_and_generate,
                                 args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # Lama导入
    def Lama_import(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=lama_upload, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # Lama导回
    def Lama_export(self):
        if running_variable.running == False:
            threads = []
            threads.append(
                threading.Thread(target=lama_download, args=(application_list, self.ui.tabWidget.currentIndex())))
            running_variable.running = True
            threads[0].start()
        else:
            print("当前已经有任务在运行了")

    # 中止当前任务
    def stop(self):
        running_variable.running = False
        print("中止当前执行的任务")

    def main_tool_bar(self):
        # 绑定工具栏的功能
        self.ui.actionadd_control.triggered.connect(lambda: add_cn_preset_win(self, application_list))
        self.ui.actionadd_preset.triggered.connect(lambda: add_preset_win(self, application_list))
        self.ui.action_optop.triggered.connect(lambda: toggle_topmost(self))
        self.ui.action_to_night_2.triggered.connect(lambda: repair_is_night(True))
        self.ui.action_to_early.triggered.connect(lambda: repair_is_night(False))
        self.ui.action_to_by_win.triggered.connect(lambda: self.init_sub_win())
        self.ui.actionopcacity_true.triggered.connect(lambda: repair_is_opacity(True,self))
        self.ui.actionopcacity_false.triggered.connect(lambda: repair_is_opacity(False,self))

        # 绑定副窗口工作栏功能
        # self.ui_small.action_to_main_win.triggered.connect(lambda: self.change_main_window())

        # 绑定开始批量操作
        self.ui.start_all.clicked.connect(lambda: self.deal_all_method())
        self.ui.stop_all.clicked.connect(lambda: self.stop_all_method())

        # 设置是否播放声音
        self.ui.actionyinpin_start.triggered.connect(lambda: repair_is_sound(True))
        self.ui.actionyinpin_stop.triggered.connect(lambda: repair_is_sound(False))

        # 存档
        self.ui.actionsave.triggered.connect(lambda: save_project(self, application_list))
        self.ui.actionimport.triggered.connect(lambda: import_project(self, application_list))
        self.ui.actionexit.triggered.connect(lambda: app.quit())

        shortcut = QShortcut(QKeySequence('Ctrl+s'), self)
        shortcut.activated.connect(lambda: save_project(self, application_list))
        shortcut1 = QShortcut(QKeySequence('Ctrl+r'), self)
        shortcut1.activated.connect(lambda: import_project(self, application_list))
        shortcut2 = QShortcut(QKeySequence('Ctrl+q'), self)
        shortcut2.activated.connect(lambda: app.quit())

        def check_block():
            global is_block
            is_block = self.ui.is_block_short_key.isChecked()
        self.ui.is_block_short_key.stateChanged.connect(lambda: [check_block(),self.block_all_short_key()])

    def block_all_short_key(self):
        global is_block
        # 开启状态屏蔽掉所有快捷键
        if is_block:
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
        # 取消屏蔽状态后更新当前页面的快捷键
        else:
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                data = json.load(f)
                setting = data["settings"][application_list[self.ui.tabWidget.currentIndex()].preset_combo.currentIndex()]
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
            keyboard.add_hotkey(setting["hotkey1"], lambda: self.short_key_import_sd())
            keyboard.add_hotkey(setting["hotkey2"], lambda: self.import_back_ps())
            keyboard.add_hotkey(setting["hotkey3"], lambda: self.start_caculate())
            keyboard.add_hotkey("ctrl+shift+f3", lambda: self.Lama_import())
            keyboard.add_hotkey("ctrl+shift+f4", lambda: self.Lama_export())

    def init_sub_win(self):
        repair_pswindow(True)
        self.a = small_windows(self)

    def tabs_bind(self):
        # 对于每个tab执行的方法
        # 更改标签名
        self.ui_tab_w.rename_tab.clicked.connect(
            lambda: self.rename_tab(application_list))
        self.ui_tab_w.tab_name.returnPressed.connect(lambda: self.rename_tab(application_list))
        # 读取config.json文件,更改预设的列表
        BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
            data = json.load(f)
            now_preset = data["setting_index"]
            preset_list = data["settings"]
        all_preset_name = []
        for i in preset_list:
            all_preset_name.append(i["name"])
        self.ui_tab_w.preset_combo.addItems(all_preset_name)
        self.ui_tab_w.preset_combo.setCurrentIndex(now_preset)

        # 更改重绘幅度
        self.ui_tab_w.paint_weight.setText(data["am"])

        # 更改张数
        self.ui_tab_w.paint_count.setText(data["ct"])

        # 更改weburl
        self.ui_tab_w.webui_url.setText(data["url"])

        # 更改autodlid
        if "autodl" in data:
            self.ui_tab_w.autodl_id.setText(data["autodl"])

        # 启用高清放大
        self.ui_tab_w.is_hd.setChecked(data["hd"])

        # 更改低清放大幅度
        self.ui_tab_w.hd_weight.setText(data["hdam"])

        # 更改controlnet
        with open(os.path.join(BASE_PATH, "ControlNet.json"), "r") as f:
            data_control = json.load(f)
        cn_list = []
        cn_list.append("无")
        for i in data_control:
            cn_list.append(i["name"])
        self.ui_tab_w.cn0_preset.addItems(cn_list)
        self.ui_tab_w.cn1_preset.addItems(cn_list)
        self.ui_tab_w.cn2_preset.addItems(cn_list)
        self.ui_tab_w.cn3_preset.addItems(cn_list)
        self.ui_tab_w.cn0_preset.setCurrentIndex(data["control_index"])
        self.ui_tab_w.cn1_preset.setCurrentIndex(0)
        self.ui_tab_w.cn2_preset.setCurrentIndex(0)
        self.ui_tab_w.cn3_preset.setCurrentIndex(0)

        # 设置lama url
        self.ui_tab_w.lama_url.setText(data["lama_url"])

        # 连接tab上的预设设置按钮
        self.ui_tab_w.set_preset.clicked.connect(
            lambda: open_set_preset(self, self.ui_tab_w.preset_combo.currentIndex(), application_list))

        # 连接设置预设按钮
        self.ui_tab_w.cn0_preset_set_btn.clicked.connect(
            lambda: set_cn_win(self, self.ui_tab_w.cn0_preset.currentIndex(), application_list))
        self.ui_tab_w.cn1_preset_set_btn.clicked.connect(
            lambda: set_cn_win(self, self.ui_tab_w.cn1_preset.currentIndex(), application_list))
        self.ui_tab_w.cn2_preset_set_btn.clicked.connect(
            lambda: set_cn_win(self, self.ui_tab_w.cn2_preset.currentIndex(), application_list))
        self.ui_tab_w.cn3_preset_set_btn.clicked.connect(
            lambda: set_cn_win(self, self.ui_tab_w.cn3_preset.currentIndex(), application_list))

        # 控制重绘幅度和张数的输入范围
        self.ui_tab_w.paint_count.setValidator(QIntValidator(1, 9999999))
        self.reg = QRegularExpression('^0\.(0[1-9]|[1-9]\d?)$|^1\.00$')
        self.validator = QRegularExpressionValidator()
        self.validator.setRegularExpression(self.reg)
        self.ui_tab_w.paint_weight.setValidator(self.validator)
        self.ui_tab_w.hd_weight.setValidator(self.validator)

        # 自动匹配文件名
        self.ui_tab_w.auto_layer_name.clicked.connect(lambda: auto_doc_name(application_list))
        # 全应用该url和id
        self.ui_tab_w.all_url_btn.clicked.connect(
            lambda: all_url_method(self.ui.tabWidget.currentIndex(), application_list))
        self.ui_tab_w.all_hd_btn.clicked.connect(
            lambda: all_hd_method(self.ui.tabWidget.currentIndex(), application_list))
        self.ui_tab_w.all_num_btn.clicked.connect(
            lambda: all_num_method(self.ui.tabWidget.currentIndex(), application_list))

        # 运算按钮
        self.ui_tab_w.import_sd_btn.clicked.connect(
            lambda: self.short_key_import_sd())
        self.ui_tab_w.start_cal_btn.clicked.connect(
            lambda: self.start_caculate())
        self.ui_tab_w.only_import_btn.clicked.connect(
            lambda: self.only_import())
        self.ui_tab_w.only_import_start.clicked.connect(
            lambda: self.only_import_start())
        self.ui_tab_w.back_ps_btn.clicked.connect(
            lambda: self.import_back_ps())
        self.ui_tab_w.hd_btn.clicked.connect(
            lambda: self.hd_back_ps_btn())
        self.ui_tab_w.stop_project_btn.clicked.connect(
            lambda: self.stop())
        self.ui_tab_w.lama_import.clicked.connect(
            lambda: self.Lama_export())
        self.ui_tab_w.lama_export.clicked.connect(
            lambda: self.Lama_import())

        # 存档
        self.ui_tab_w.export_project_btn.clicked.connect(
            lambda: save_project_self(self, application_list, self.ui.tabWidget.currentIndex()))

    def closeEvent(self, event):
        try:
            BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
            with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
                data = json.load(f)
                data["setting_index"] = application_list[0].preset_combo.currentIndex()
                data["am"] = application_list[0].paint_weight.text()
                data["ct"] = application_list[0].paint_count.text()
                data["url"] = application_list[0].webui_url.text()
                data["hd"] = application_list[0].is_hd.isChecked()
                data["hdam"] = application_list[0].hd_weight.text()
                data["control_index"] = application_list[0].cn0_preset.currentIndex()
                data["lama_url"] = application_list[0].lama_url.text()
            with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
                # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
                formatted_data = json.dumps(data, indent=4)
                # 将格式化后的 json 字符串写入新的文件
                f.write(formatted_data)
            event.accept()
        except:
            event.accept()


def exceptOutConfig(exctype, value, tb):
    traceback.print_exc(tb)


def check_pswindow():
    global ispswindow
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
    ispswindow=data["ispswindow"]

def repair_pswindow(is_ps):
    global ispswindow
    ispswindow=is_ps
    if is_ps:
        print("更改为ps插件窗口")
    else:
        print("更改为主窗口")
    BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f:
        data = json.load(f)
        data["ispswindow"]=is_ps
    with open(os.path.join(BASE_PATH, "config.json"), "w") as f:
        # 将 python 字典转换为 json 字符串，并指定缩进为 4 个空格
        formatted_data = json.dumps(data, indent=4)
        # 将格式化后的 json 字符串写入新的文件
        f.write(formatted_data)

if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    sys.excepthook = exceptOutConfig
    app = QApplication(sys.argv)
    check_is_sound()
    check_pswindow()
    # 查看是否透明
    check_opacity()
    w = Main_windows()
    # w.show()
    # 查看昼夜模式
    check_is_night()
    night_theme()
    # 设置为置顶
    toggle_topmost(w)
    w.first_boot()
    sys.exit(app.exec_())
