from PySide6.QtWidgets import QFrame, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from qfluentwidgets import (BodyLabel,SubtitleLabel, PushButton, InfoBar, InfoBarPosition)

from task.keyboar_recorder import KeyboardRecorder

class ScriptMacrosInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ScriptMacrosInterface")
        self.recorder_thread = None
        self.is_recording = False

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.addWidget(SubtitleLabel("脚本宏"))
        self.vBoxLayout.addSpacing(10) 
        self.recordButton = PushButton("录制")
        self.recordLabel = BodyLabel("")
        self.recordButton.setFixedWidth(80)
        self.vBoxLayout.addWidget(self.recordButton)
        self.vBoxLayout.addWidget(self.recordLabel)

        self.vBoxLayout.addStretch(1)
        self.setLayout(self.vBoxLayout)
        self.recordButton.clicked.connect(self.start_recording)

    def start_recording(self):
        self.recorder_thread = KeyboardRecorder("key_events")
        self.recorder_thread.recording_status_changed.connect(self.update_label)
        self.recorder_thread.start()
        self.is_recording = True
        self.recordButton.setDisabled(True)

    def update_label(self, message):
        print(message)
        if message == "stop":
            self.stop_recording()
        elif message == "record":
            self.recordLabel.setText("脚本录制中，按下 Home 停止录制")
        else:
            self.recordLabel.setText("脚本录制进程已经启动，按下 Home 开始录制")

    def stop_recording(self):
        self.recorder_thread.stop()
        self.is_recording = False
        self.recordButton.setDisabled(False)
        self.recordLabel.hide()
        InfoBar.success(
            title="脚本录制完成",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )
