
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, ScrollArea, BodyLabel, ComboBox, SwitchButton, ImageLabel, PushSettingCard, InfoBar, InfoBarPosition
from task.hotkey_thread import HotkeyThread
from module.gw2 import gw2_instance
from utils.utils import root_path

class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.gw2_instance = gw2_instance
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        image = ImageLabel(os.path.join(root_path(), "assets", "logo.png"))
        image.scaledToHeight(100)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("HomeInterface")
        
        self.runButton = PushSettingCard(
            text="启动",
            icon=FluentIcon.GAME,
            title="激战2",
            content="怕就别用, 用就别怕！"
        )

        self.runButton.clicked.connect(self.start_game)
        self.vBoxLayout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addSpacing(10) 
        self.vBoxLayout.addWidget(self.runButton)
        # self.vBoxLayout.addWidget(FastOperationCard())
        self.vBoxLayout.addStretch(1)
        self.enableTransparentBackground()

    def start_game(self):
        gw2_instance.get_hwnd()
        hwnd = gw2_instance.hwnd
        if hwnd is None or hwnd == 0:
            InfoBar.error(
                title='启动失败',
                content="Bro 你需要先启动游戏哦~！",
                orient=Qt.Vertical,  # 内容太长时可使用垂直布局
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000, 
                parent=self
            )
        else:
            self.runButton.setEnabled(False)
            self.runButton.button.setText("已启动")
            
class FastOperationCard(ExpandGroupSettingCard):
    
    def __init__(self, parent=None):
        super().__init__(FluentIcon.SPEED_OFF, "背包右键快速操作", "选中背包物品后通过快捷键进行快速操作, 快捷键为 F11 ", parent)
        self.setObjectName("FastOperationCard")

        self.operationTypeLabel = BodyLabel("操作类型")
        self.operationTypeComboBox = ComboBox()
        self.operationTypeComboBox.addItems(["摧毁"])
        self.operationTypeComboBox.setFixedWidth(100)

        # self.destroyConfirmationLabel = BodyLabel("二次确认摧毁？")
        # self.destroyConfirmatioButton = SwitchButton()
        # self.destroyConfirmatioButton.setOffText("")
        # self.destroyConfirmatioButton.setOnText("")

        self.operationLabel = BodyLabel("背包右键操作")
        self.operationButton = SwitchButton()
        self.operationButton.setOffText("")
        self.operationButton.setOnText("")

        self.operationButton.checkedChanged.connect(self.start_fast_operation)
        self.viewLayout.setSpacing(0)

        self.add(self.operationTypeLabel, self.operationTypeComboBox)
        # self.add(self.destroyConfirmationLabel, self.destroyConfirmatioButton)
        self.add(self.operationLabel, self.operationButton)

    def add(self, label, widget):
        w = QWidget()
        w.setFixedHeight(60)
        layout = QHBoxLayout(w)
        layout.setContentsMargins(48, 12, 48, 12)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(widget)
        self.addGroupWidget(w)

    
    def start_fast_operation(self, checked):
        self.thread = HotkeyThread(checked)
        self.thread.finished.connect(self.on_hotkey_setup_complete)
        self.thread.start()

    def on_hotkey_setup_complete(self, success):
        if success:
            print("开始快速操作" if success else "停止快速操作")