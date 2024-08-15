from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QHeaderView, QTableWidgetItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (BodyLabel,SubtitleLabel, PushButton,TableWidget)
from module.config import Config
from task.keyboar_recorder import KeyboardRecorder

config = Config()

class ScriptMacrosInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosInterface")
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
            print("remove")
            script_macros = config.get("script_macros")
            del script_macros[index]
            print(script_macros)
            config.set("script_macros", script_macros)
            self.table.update_table(config.get("script_macros"))
        elif type == "record":
            print("record")
    
    def header_info_signal_handler(self, type):
        if type == "create":
            print("create")
            script_macros = config.get("script_macros")
            script_macros.append({"name": "新建脚本宏", "desc": "请录制脚本宏"})
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
        self.vBoxLayout.addWidget(BodyLabel("创建脚本宏选择脚本宏后，选择脚本宏名称录制脚本宏, 录制会覆盖当前脚本宏内容。"))
        self.vBoxLayout.addSpacing(10) 
        self.createButton = PushButton("创建脚本宏")
        self.createButton.setFixedWidth(100)
        self.vBoxLayout.addWidget(self.createButton)
        self.setLayout(self.vBoxLayout)
        self.createButton.clicked.connect(self.create_script_macro)

    def create_script_macro(self):
        # 发出信号出去
        self.header_info_signal.emit("create")

class ScriptMacrosTableWidget(QWidget):

    table_signal = Signal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosTableWidget")

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.table = TableWidget(self)
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 260)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(2, 140)
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

            desc_item = QTableWidgetItem(item["desc"])
            desc_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(i, 1, desc_item)

            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            record_button = PushButton("录制", self)
            record_button.setFixedWidth(60)
            record_button.setFixedHeight(30)

            remove_button = PushButton("删除", self)
            remove_button.setFixedWidth(60)
            remove_button.setFixedHeight(30)
            hbox.addWidget(record_button)
            hbox.addSpacing(10) 
            hbox.addWidget(remove_button)

            record_button.clicked.connect(lambda: self.record_button(i))
            remove_button.clicked.connect(lambda: self.remove_script_macro(i))

            cell_widget = QWidget()
            cell_widget.setLayout(hbox)
            self.table.setCellWidget(i, 2, cell_widget)

    def remove_script_macro(self, index):
        # 发出信号出去
        self.table_signal.emit(index, "remove")

    def record_button(self, index):
        self.table_signal.emit(index, "record")
  