import sys
import json
import time
from PySide6.QtCore import QThread, Signal, QWaitCondition, QMutex
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from pynput import keyboard

class KeyboardRecorder(QThread):
    recording_status_changed = Signal(str)  # 用于通知主线程状态的信号

    def __init__(self):
        super().__init__()
        self.key_events = []
        self.last_time = None
        self.listening = False
        self.pressed_keys = set()
        self.stop_request = False  # 用于通知线程停止的标志
        self.mutex = QMutex()  # 线程安全的互斥锁
        self.wait_condition = QWaitCondition()  # 用于线程等待的条件

    def on_press(self, key):
        if key == keyboard.Key.home:
            if not self.listening:
                # 开始录制
                print("开始监听按键事件...")
                self.listening = True
                self.last_time = None
                self.pressed_keys.clear()
                self.recording_status_changed.emit("start")
            else:
                # 停止录制
                print("停止监听按键事件...")
                self.listening = False
                self.save_to_json()
                self.recording_status_changed.emit("stop")
            return

        if self.listening and key not in self.pressed_keys:
            current_time = time.time()
            interval = round(current_time - self.last_time, 2) if self.last_time is not None else 0.00

            self.key_events.append({
                'event': 'press',
                'key': str(key),
                'interval': interval
            })

            self.last_time = current_time
            self.pressed_keys.add(key)

    def on_release(self, key):
        if self.listening and key in self.pressed_keys:
            current_time = time.time()
            interval = round(current_time - self.last_time, 2) if self.last_time is not None else 0.50

            self.key_events.append({
                'event': 'release',
                'key': str(key),
                'interval': interval
            })

            self.last_time = current_time
            self.pressed_keys.remove(key)

    def save_to_json(self):
        with open(f'{self.file_name}.json', 'w') as f:
            json.dump(self.key_events, f, indent=4)
        print(f"按键事件已保存到 {self.file_name}.json")

    def run(self):
        # 监听键盘事件
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while not self.stop_request:
                self.mutex.lock()
                self.wait_condition.wait(self.mutex)  # 等待停止信号
                self.mutex.unlock()
                if self.stop_request:
                    break
            listener.stop()

    def stop(self):
        self.mutex.lock()
        self.stop_request = True
        self.wait_condition.wakeAll()  # 唤醒等待中的线程
        self.mutex.unlock()
        self.wait()  # 等待线程安全退出
        print("线程安全退出")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keyboard Recorder")

        self.label = QLabel("Press Home key to start recording...")
        self.recordButton = QPushButton("Start Recording")
        self.recordButton.clicked.connect(self.toggle_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.recordButton)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.recorder_thread = None
        self.is_recording = False

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recorder_thread = KeyboardRecorder("key_events")
        self.recorder_thread.recording_status_changed.connect(self.update_label)
        self.recorder_thread.start()
        self.is_recording = True
        self.recordButton.setText("Stop Recording")

    def stop_recording(self):
        if self.recorder_thread:
            self.recorder_thread.stop()
        self.is_recording = False
        self.recordButton.setText("Start Recording")

    def update_label(self, message):
        if message == "stop":
            self.stop_recording()
        elif message == "start":
            self.label.setText("Recording started. Press Home to stop.")
        else:
            self.label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
