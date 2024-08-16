import time
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QHeaderView, QTableWidgetItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (BodyLabel,SubtitleLabel, PushButton,TableWidget, InfoBar, InfoBarPosition, window)
from module.config import Config
from task.keyboar_recorder import KeyboardRecorder
from task.run_script_macros import RunScriptMacrosThread

config = Config()

class ScriptMacrosInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosInterface")

        self.keyboard_recorder = None
        self.test_script_macros = None

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.headerWidget = HeaderInfoWidgtet(self)
        self.table = ScriptMacrosTableWidget(self)
        self.vBoxLayout.addWidget(self.headerWidget)
        self.vBoxLayout.addWidget(self.table)
        self.table.update_table(config.get("script_macros"))
        self.table.table_signal.connect(self.table_signal_handler)
        self.headerWidget.header_info_signal.connect(self.header_info_signal_handler)

    def table_signal_handler(self, index, type):
        if type == "remove":
            script_macros = config.get("script_macros")
            del script_macros[index]
            config.set("script_macros", script_macros)
            self.table.update_table(config.get("script_macros"))
        if type == "test":
            time.sleep(2)
            self.test_script_macros = RunScriptMacrosThread(config.get("script_macros")[index]["script"])
            self.test_script_macros.start()

    def header_info_signal_handler(self, type):
        if type == "create":
            self.recorder_thread = KeyboardRecorder()
            self.recorder_thread.start()
            self.recorder_thread.record_done.connect(self.recorder_thread_done)
        else:
            if self.recorder_thread is not None:
                self.recorder_thread.stop()

    def recorder_thread_done(self, script):
        self.recorder_thread.stop()
        self.headerWidget.createButton.setDisabled(False)
        self.headerWidget.stop_recording()
        script_macros = config.get("script_macros")
        script_macros.append({"name": "新建脚本宏", "script": script})
        config.set("script_macros", script_macros)
        self.table.update_table(config.get("script_macros"))


class HeaderInfoWidgtet(QWidget):
    header_info_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosCreateWidgtet")
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(SubtitleLabel("脚本宏"))
        self.vBoxLayout.addSpacing(10) 
        self.vBoxLayout.addWidget(BodyLabel("点击创建脚本，按下 Home 键开始录制，再次按下 Home 键结束录制，即可创建脚本宏。"))
        self.vBoxLayout.addSpacing(10) 
        self.createButton = PushButton("创建脚本宏")
        self.createButton.setFixedWidth(100)

        self.createButton.clicked.connect(self.create_script_macro)
        self.stopButton = PushButton("停止录制")
        self.stopButton.setDisabled(True)
        self.stopButton.clicked.connect(self.stop_recording)
        self.stopButton.setFixedWidth(100)

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.createButton)
        self.hBoxLayout.addWidget(self.stopButton)
        self.hBoxLayout.addStretch(1)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.setLayout(self.vBoxLayout)

    def stop_recording(self):
        self.createButton.setDisabled(False)
        self.stopButton.setDisabled(True)
        self.header_info_signal.emit("stop")

    def create_script_macro(self):
        self.createButton.setDisabled(True)
        self.stopButton.setDisabled(False)
        self.header_info_signal.emit("create")

class ScriptMacrosTableWidget(QWidget):

    table_signal = Signal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosTableWidget")

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.table = TableWidget(self)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 160)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vBoxLayout.addWidget(self.table)
        self.setLayout(self.vBoxLayout)

    def update_table(self, data):
        self.table.setRowCount(len(data))

        for i, item in enumerate(data):
            name_item = QTableWidgetItem(item["name"])
            name_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(i, 0, name_item)

            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            test_button = PushButton("测试", self)
            test_button.setFixedWidth(60)
            test_button.setFixedHeight(30)
            test_button.clicked.connect(lambda: self.button_clicked(i, "test"))

            remove_button = PushButton("删除", self)
            remove_button.setFixedWidth(60)
            remove_button.setFixedHeight(30)
            hbox.addWidget(test_button)
            hbox.addSpacing(18) 
            hbox.addWidget(remove_button)

            remove_button.clicked.connect(lambda: self.button_clicked(i, "remove"))

            cell_widget = QWidget()
            cell_widget.setLayout(hbox)
            self.table.setCellWidget(i, 1, cell_widget)

    def button_clicked(self, index, type):
        # self.table.setDisabled(True)
        self.table_signal.emit(index, type)
