from PySide6.QtCore import QThread, Signal
import keyboard

from fast_operate import right_operate_destroy

class HotkeyThread(QThread):
    finished = Signal(bool)

    def __init__(self, enable_hotkey):
        super().__init__()
        self.enable_hotkey = enable_hotkey

    def run(self):
        if self.enable_hotkey:
            keyboard.add_hotkey("F11", right_operate_destroy)
        else:
            keyboard.remove_hotkey("F11")
        self.finished.emit(self.enable_hotkey)