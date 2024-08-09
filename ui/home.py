import keyboard
from qfluentwidgets import (setFont, SubtitleLabel)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFrame
from qfluentwidgets import FluentIcon, PushSettingCard, ExpandGroupSettingCard, ScrollArea, BodyLabel, ComboBox, SwitchButton, ImageLabel, InfoBar, InfoBarPosition

from fast_operate import right_operate_destroy
from utils.utils import get_hwnd


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.runButton = PushSettingCard(
            text="启动",
            icon=FluentIcon.GAME,
            title="激战2",
            content="怕就别用, 用就别怕！"
        )

        image = ImageLabel("./assets/logo.png")
        image.scaledToHeight(100)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("HomeInterface")
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20) 
        self.vBoxLayout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addSpacing(10) 
        self.vBoxLayout.addWidget(self.runButton)
        
        self.vBoxLayout.addWidget(FastOperationCard())
        self.vBoxLayout.addStretch(1)
        self.enableTransparentBackground()

        self.runButton.clicked.connect(self.start_game)


    def start_game(self):
        hwnd = get_hwnd()
        if hwnd is not None:
            self.runButton.button.setText("停止") 
        else:
            self.runButton.button.setText("启动")
            InfoBar.warning(
                title=self.tr('启动失败, 请检查游戏是否已启动'),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )

class FastOperationCard(ExpandGroupSettingCard):
    
    def __init__(self, parent=None):
        super().__init__(FluentIcon.SPEED_OFF, "背包右键快速操作", "选中背包物品后通过快捷键进行快速操作, 快捷键为 F11 ", parent)
        self.setObjectName("FastOperationCard")

        self.operationTypeLabel = BodyLabel("操作类型")
        self.operationTypeComboBox = ComboBox()
        self.operationTypeComboBox.addItems(["销毁", "出售"])
        self.operationTypeComboBox.setFixedWidth(100)

        self.destroyConfirmationLabel = BodyLabel("二次确认摧毁？")
        self.destroyConfirmatioButton = SwitchButton()
        self.destroyConfirmatioButton.setOffText("")
        self.destroyConfirmatioButton.setOnText("")

        self.operationLabel = BodyLabel("背包右键操作")
        self.operationButton = SwitchButton()
        self.operationButton.setOffText("")
        self.operationButton.setOnText("")

        self.operationButton.checkedChanged.connect(self.start_fast_operation)

        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        # 添加各组到设置卡中
        self.add(self.operationTypeLabel, self.operationTypeComboBox)
        self.add(self.destroyConfirmationLabel, self.destroyConfirmatioButton)
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
        if checked:
            keyboard.add_hotkey("F11", right_operate_destroy)
            print("开始快速操作")
        else:
            keyboard.remove_hotkey("F11")
            print("停止快速操作")