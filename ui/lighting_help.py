from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,  QTableWidgetItem, QHeaderView, QSizePolicy, QSizePolicy, QApplication
from qfluentwidgets import FluentIcon , PushButton, LineEdit, ComboBox, BodyLabel, ToolButton, TableWidget, InfoBar, InfoBarPosition
from task.detection_thread import DetectionLightingThread

light_comboBox_list = ['照亮天空哨站群岛', '照亮阿姆尼塔斯', '照亮纳约斯内层']
class LightingHelpInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("LightingHelpInterface")
        self.vBoxLayout = QVBoxLayout(self)
        self.floadWidget = FloadWidget()
        self.floadWidget.detection_signal.connect(self.on_detection_signal)
        self.detectionTableWidget = DetectionTableWidget()
        self.vBoxLayout.addWidget(self.floadWidget)
        self.vBoxLayout.addWidget(self.detectionTableWidget)
        self.vBoxLayout.setStretch(0, 0)  
        self.vBoxLayout.setStretch(1, 1)

    def on_detection_signal(self, fload, achievement):
        if fload != "" and achievement != "":
            InfoBar.info(
                title='检测完成后下方会展示未完成的成就',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            not_done_list = []
            self.detection_list_update(not_done_list)

            self.detection_thread = DetectionLightingThread(fload, achievement)
            self.detection_thread.detectionFinished.connect(self.detection_list_update)
            self.detection_thread.finished.connect(self.setButtonEnabled)
            self.detection_thread.start()

    def setButtonEnabled(self):
        self.floadWidget.detectionButton.setEnabled(True)

    def detection_list_update(self, detection_list):
        self.detectionTableWidget.update_table(detection_list)

class FloadWidget(QWidget):
    detection_signal = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("FloadWidget")

        self.achievementComboBoxValue = light_comboBox_list[0]
        self.vBoxLayout = QVBoxLayout(self)

        # 图片目录部分
        self.floadLabel = BodyLabel("目录：", self)
        self.floadLabel.setFixedWidth(60)
        self.floadButton = ToolButton(FluentIcon.FOLDER, self)
        self.floadLineEdit = LineEdit(self) 
        self.floadLineEdit.setFixedWidth(400)
        self.floadLineEdit.setPlaceholderText("请选择图片目录")
        self.floadButton.clicked.connect(self.floadButtonClicked)

        # 图片目录的水平布局
        self.floadHBoxLayout = QHBoxLayout()
        self.floadHBoxLayout.addWidget(self.floadLabel)
        self.floadHBoxLayout.addWidget(self.floadLineEdit)
        self.floadHBoxLayout.addWidget(self.floadButton)
        self.floadHBoxLayout.addStretch(1)

        # 成就列表部分
        self.achievementComboBox = ComboBox()
        self.achievementComboBox.addItems(light_comboBox_list)
        self.achievementLabel = BodyLabel("成就：", self)
        self.achievementLabel.setFixedWidth(60)
        self.achievementComboBox.currentIndexChanged.connect(self.achievementComboBoxChanged)

        # 成就的水平布局
        self.achievementHBoxLayout = QHBoxLayout()
        self.achievementHBoxLayout.addWidget(self.achievementLabel)
        self.achievementHBoxLayout.addWidget(self.achievementComboBox)
        self.achievementHBoxLayout.addStretch(1)    
        # 设置边距
        self.achievementHBoxLayout.setContentsMargins(0, 4, 0, 0)
        # 照亮按钮部分
        self.detectionButton = PushButton("检测", self)
        self.detectionButton.clicked.connect(self.emit_detection_signal)  # 连接点击信号
        self.detectionButton.setFixedWidth(80)

        # 检测按钮的水平布局
        self.detectionHBoxLayout = QHBoxLayout()
        self.detectionHBoxLayout.addWidget(self.detectionButton)
        self.detectionHBoxLayout.addStretch(1)

        # 将所有子布局添加到主布局
        self.vBoxLayout.addLayout(self.floadHBoxLayout)
        self.vBoxLayout.addLayout(self.achievementHBoxLayout)
        self.vBoxLayout.addLayout(self.detectionHBoxLayout)

        self.setLayout(self.vBoxLayout)  # 设置主布局

    def floadButtonClicked(self):
        # qt 打开文件选择框
        qFileDialog = QFileDialog()
        qFileDialog.setFileMode(QFileDialog.Directory)
        qFileDialog.setOption(QFileDialog.ShowDirsOnly, True)
        if qFileDialog.exec():
            fileNames = qFileDialog.selectedFiles()
            self.floadLineEdit.setText(fileNames[0])

    def achievementComboBoxChanged(self):
        self.achievementComboBoxValue = self.achievementComboBox.currentText()
    
    def emit_detection_signal(self):
        fload = self.floadLineEdit.text()
        achievement = self.achievementComboBoxValue
        if fload == "":
            InfoBar.error(
                title='请选择图片目录',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return
        
        self.detectionButton.setEnabled(False)
        self.detection_signal.emit(fload, achievement)  # 发出信号


class DetectionTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("DetectionListWidget")
        self.vBoxLayout = QVBoxLayout(self)

        self.detectionListLabel = BodyLabel("", self)
        self.detectionListLabel.hide()
        self.detectionListLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.table = TableWidget(self)
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 260)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(2, 100)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vBoxLayout.addWidget(self.detectionListLabel)
        self.vBoxLayout.addWidget(self.table)
        self.setLayout(self.vBoxLayout)

    def update_table(self, detection_list):
        self.detection_list = detection_list

        if len(detection_list) == 0:
            self.detectionListLabel.hide()
            self.table.clear()
            return

        self.detectionListLabel.setText(f"检测到 {len(detection_list)} 个未完成的成就")
        self.detectionListLabel.show()
        self.table.setRowCount(len(detection_list))
        
        for i, item in enumerate(detection_list):
            objective = item.get('Objective', '')
            game_link = item.get('Game_link', '')
            self.table.setItem(i, 0, QTableWidgetItem(objective))
            self.table.setItem(i, 1, QTableWidgetItem(game_link))
            copy_button = PushButton("复制", self)
            copy_button.setFixedWidth(60)
            copy_button.setFixedHeight(30)
            copy_button.clicked.connect(lambda checked, row=i: self.copy_item(row))
            self.table.setCellWidget(i, 2, copy_button)

    def copy_item(self, row):
        if 0 <= row < len(self.detection_list):
            item = self.detection_list[row]
            clipboard = QApplication.clipboard()
            clipboard.setText(item.get('Game_link', ''))