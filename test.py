# import json
# from pynput import keyboard
# import time
# import signal
# import sys

# # 记录按键的状态和时间戳
# key_events = []
# last_time = None
# listening = False  # 监听状态
# pressed_keys = set()  # 记录当前被按下的按键

# def on_press(key):
#     global last_time, listening
    
#     # 切换监听状态
#     if key == keyboard.Key.home:
#         listening = not listening
#         if listening:
#             print("开始监听按键事件...")
#             last_time = None  # 重置 last_time
#             pressed_keys.clear()  # 清空已按下的按键
#         else:
#             print("停止监听按键事件...")
#             save_to_json()
#         return
    
#     if listening and key not in pressed_keys:
#         current_time = time.time()
        
#         if last_time is not None:
#             interval = current_time - last_time
#         else:
#             interval = None
        
#         key_events.append({
#             'event': 'press',
#             'key': str(key),
#             'time': current_time,
#             'interval': interval
#         })
        
#         last_time = current_time
#         pressed_keys.add(key)  # 记录按下的按键

# def on_release(key):
#     global last_time
    
#     if listening and key in pressed_keys:
#         current_time = time.time()
        
#         if last_time is not None:
#             interval = current_time - last_time
#         else:
#             interval = None
        
#         key_events.append({
#             'event': 'release',
#             'key': str(key),
#             'time': current_time,
#             'interval': interval
#         })
        
#         last_time = current_time
#         pressed_keys.remove(key)  # 移除已释放的按键

# def save_to_json():
#     with open('key_events.json', 'w') as f:
#         json.dump(key_events, f, indent=4)
#     print("按键事件已保存到 key_events.json")

# def signal_handler(sig, frame):
#     print('捕获到 Ctrl + C, 保存按键事件并退出...')
#     save_to_json()
#     sys.exit(0)

# # 注册信号处理，以捕获 Ctrl + C
# signal.signal(signal.SIGINT, signal_handler)

# # 监听键盘事件
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()

import json
import time
from pynput import keyboard
import threading
import os

keyboard_controller = keyboard.Controller()
executing = False
stop_execution = False
listener_thread = None

def execute_key_events(key_events):
    global stop_execution
    for event in key_events:
        if stop_execution:
            print("操作已中止.")
            break

        key = event['key']
        interval = event['interval']

        if interval is not None:
            time.sleep(interval)

        if event['event'] == 'press':
            if "Key." in key:  # 处理特殊键
                exec(f"keyboard_controller.press({key})")
            else:
                keyboard_controller.press(key.replace("'", ""))
        elif event['event'] == 'release':
            if "Key." in key:  # 处理特殊键
                exec(f"keyboard_controller.release({key})")
            else:
                keyboard_controller.release(key.replace("'", ""))

def on_press(key):
    global executing, stop_execution
    if key == keyboard.Key.home:
        if not executing:
            print("开始执行按键事件...")
            executing = True
            stop_execution = False

            # 启动新的线程来执行按键事件
            execution_thread = threading.Thread(target=execute_key_events_from_file)
            execution_thread.start()
        else:
            print("停止执行按键事件...")
            stop_execution = True
            executing = False

def execute_key_events_from_file():
    # 读取 JSON 文件
    with open('key_events.json', 'r') as f:
        key_events = json.load(f)

    # 执行键盘事件
    execute_key_events(key_events)

    global executing
    executing = False
    print("按键事件执行完毕.")

def on_release(key):
    pass

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    try:
        listener_thread = threading.Thread(target=start_listener)
        listener_thread.start()

        # 主线程可以继续执行其他任务，或等待结束
        while listener_thread.is_alive():
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n程序已终止.")
        stop_execution = True
        if listener_thread.is_alive():
            listener_thread.join()  # 等待监听器线程结束
        os._exit(0)  # 强制终止程序
