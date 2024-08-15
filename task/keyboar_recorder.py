import sys
import json
import time
from PySide6.QtCore import QThread, Signal, QWaitCondition, QMutex
from pynput import keyboard

class KeyboardRecorder(QThread):
    recording_status_changed = Signal(str)  # 用于通知主线程状态的信号

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
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
                self.recording_status_changed.emit("record")
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
        self.recording_status_changed.emit("start")
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
