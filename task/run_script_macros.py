
from PySide6.QtCore import QThread, Signal

from PySide6.QtCore import QThread, Signal
import time
import keyboard

from module.gw2 import gw2_instance

class RunScriptMacrosThread(QThread):
    run_script_signal = Signal(list)

    def __init__(self, script_macros):
        super().__init__()
        self.gw2_instance = gw2_instance
        self.script_macros = script_macros

    def run(self):
        self.gw2_instance.get_hwnd()
        self.gw2_instance.activate_window()
        time.sleep(0.1)
        for i in range(100):
            for macro in self.script_macros:
                event = macro['event']
                key = macro['key'].strip("'")  # 去掉引号
                interval = macro['interval']
                time.sleep(interval)
                if event == 'press':
                    keyboard.press(key)
                elif event == 'release':
                    keyboard.release(key)

                # 可选：发射信号通知外部监听器
                self.run_script_signal.emit(macro)