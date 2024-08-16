from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,  QTableWidgetItem, QHeaderView, QSizePolicy, QSizePolicy, QApplication
from qfluentwidgets import FluentIcon , PushButton, LineEdit, ComboBox, BodyLabel, ToolButton, TableWidget, InfoBar, InfoBarPosition, SubtitleLabel
from module.config import Config
from task.detection_thread import DetectionLightingThread
from module.gw2 import gw2_instance

config = Config()
class LightingHelpInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("LightingHelpInterface")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.floadWidget = FloadWidget()
        self.detectionTableWidget = DetectionTableWidget()
        self.vBoxLayout.addWidget(self.floadWidget)
        self.vBoxLayout.addWidget(self.detectionTableWidget)
        self.floadWidget.detection_signal.connect(self.on_detection_signal)

    def on_detection_signal(self, fload, achievement):
        if fload == '':
            gw2_instance.get_hwnd()
            hwnd = gw2_instance.hwnd
            if hwnd is None or hwnd == 0:
                self.floadWidget.detectionButton.setEnabled(True)
                InfoBar.error(
                    title='启动失败',
                    content="Bro 你需要先启动游戏哦~！",
                    orient=Qt.Vertical,  # 内容太长时可使用垂直布局
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000, 
                    parent=self
                )
                return
            
        not_done_list = []
        self.detection_list_update({'data': not_done_list, "msg": '', "type": 'info'})
        self.detection_thread = DetectionLightingThread(fload, achievement)
        self.detection_thread.detectionFinished.connect(self.detection_list_update)
        self.detection_thread.finished.connect(self.setButtonEnabled)
        self.detection_thread.start()

    def setButtonEnabled(self):
        self.floadWidget.detectionButton.setEnabled(True)

    def detection_list_update(self, result):
        self.activateWindow()
     
        if result['type'] == 'error':
            InfoBar.error(
                title=result['msg'],
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )

        if result['type'] == 'success':
            InfoBar.success(
                title=result['msg'],
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
        self.detectionTableWidget.update_table(result['data'])

class FloadWidget(QWidget):
    detection_signal = Signal(str, object)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("FloadWidget")
        light_comboBox_list = [item['name'] for item in config.get("achievements")]
        
        self.achievementComboBoxValue = light_comboBox_list[0]
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.floadLabel = BodyLabel("目录：")
        self.floadLabel.setFixedWidth(40)
        self.floadButton = ToolButton(FluentIcon.FOLDER)
        self.floadLineEdit = LineEdit(self) 
        self.floadLineEdit.setFixedWidth(400)
        self.floadLineEdit.setPlaceholderText("不选择目录则会通过脚本打开游戏抓取，需要管理员运行哦~")
        self.floadButton.clicked.connect(self.floadButtonClicked)

        self.floadHBoxLayout = QHBoxLayout()
        self.floadHBoxLayout.addWidget(self.floadLabel)
        self.floadHBoxLayout.addWidget(self.floadLineEdit)
        self.floadHBoxLayout.addWidget(self.floadButton)
        self.floadHBoxLayout.addStretch(1)

        self.achievementComboBox = ComboBox()
        self.achievementComboBox.addItems(light_comboBox_list)
        self.achievementLabel = BodyLabel("成就：")
        self.achievementLabel.setFixedWidth(40)
        self.achievementComboBox.currentIndexChanged.connect(self.achievementComboBoxChanged)

        self.achievementHBoxLayout = QHBoxLayout()
        self.achievementHBoxLayout.addWidget(self.achievementLabel)
        self.achievementHBoxLayout.addWidget(self.achievementComboBox)
        self.achievementHBoxLayout.addStretch(1)    

        self.detectionButton = PushButton("检测")
        self.detectionButton.clicked.connect(self.emit_detection_signal) 
        self.detectionButton.setFixedWidth(80)

        self.vBoxLayout.addLayout(self.floadHBoxLayout)
        self.vBoxLayout.addSpacing(10) 
        self.vBoxLayout.addLayout(self.achievementHBoxLayout)
        self.vBoxLayout.addSpacing(10) 
        self.vBoxLayout.addWidget(self.detectionButton)

    def floadButtonClicked(self):
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
        achievement_name = self.achievementComboBoxValue
        achievement = next((item for item in config.get("achievements") if item['name'] == achievement_name), None)
        self.detectionButton.setEnabled(False)
        self.detection_signal.emit(fload, achievement)  # 发出信号

class DetectionTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("DetectionListWidget")
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

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
            self.table.setRowCount(0)
            self.table.clear()  
            self.table.blockSignals(False)
            self.table.clearSpans()
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