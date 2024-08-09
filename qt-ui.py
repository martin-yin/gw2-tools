import sys
import threading
import time
import keyboard
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("键盘监听器")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.checkbox = QCheckBox("启动键盘监听")
        self.checkbox.stateChanged.connect(self.toggle_key_listener)

        self.layout.addWidget(self.checkbox)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        self.listener_thread = None
        self.is_running = True
        self.main_task_thread = threading.Thread(target=self.main_task)
        self.main_task_thread.start()

    def toggle_key_listener(self, state):
        if state == 2:  # QCheckBox is checked
            self.start_key_listener()
        else:  # QCheckBox is unchecked
            self.stop_key_listener()

    def start_key_listener(self):
        if self.listener_thread is None or not self.listener_thread.is_alive():
            self.is_running = True
            self.listener_thread = threading.Thread(target=self.key_listener)
            self.listener_thread.start()

    def stop_key_listener(self):
        if self.listener_thread is not None and self.listener_thread.is_alive():
            self.is_running = False
            self.listener_thread.join()

    def key_listener(self):
        keyboard.add_hotkey("1", self.on_trigger_destroy)
        while self.is_running:
            time.sleep(0.1)  # 防止CPU占用过高
        keyboard.unhook_all_hotkeys()  # 确保热键被清除

    def on_trigger_destroy(self):
        print("销毁键被按下")

    def main_task(self):
        while self.is_running:
            print("主任务运行中...")
            time.sleep(1)

    def closeEvent(self, event):
        self.is_running = False
        if self.listener_thread is not None and self.listener_thread.is_alive():
            self.listener_thread.join()
        if self.main_task_thread is not None and self.main_task_thread.is_alive():
            self.main_task_thread.join()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())