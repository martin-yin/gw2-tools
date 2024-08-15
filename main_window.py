import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, MSFluentWindow, setTheme, Theme, FluentIcon as FIF)
from ui.home import HomeInterface
from ui.lighting_help import LightingHelpInterface
from ui.script_macros import ScriptMacrosInterface
from ui.setting import SeetingInterface
from utils.utils import root_path

class Window(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.homeInterface = HomeInterface(self)
        self.scriptMacrosInterface = ScriptMacrosInterface(self)
        self.lightingHelpInterface = LightingHelpInterface(self)
        self.seetingInterface = SeetingInterface(self)

        self.initNavigation()
        self.initWindow()
        setTheme(Theme.DARK)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.scriptMacrosInterface, FIF.ROBOT, '脚本宏')
        self.addSubInterface(self.lightingHelpInterface, FIF.VIEW, '点灯辅助')

        self.addSubInterface(self.seetingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
    
    def initWindow(self):
        self.resize(720, 520)
        self.setWindowIcon(QIcon(os.path.join(root_path(), "assets", "logo.ico")))
        self.setWindowTitle('激战2-工具箱')
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
