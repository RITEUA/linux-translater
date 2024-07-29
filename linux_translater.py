from translate import Translator
from pynput import keyboard, mouse
import subprocess

# Множина для зберігання підходящих гарячих клавіш (alt, shift, t)
keys_pressed = set()


# Отримуємо виділений текст
def get_selected_text():
    result = subprocess.run(['xclip', '-o'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')
    

# Функція для перекладу виділеного тексту
def translate():
    translator = Translator(to_lang="uk")
    selected_text = get_selected_text()
    result = translator.translate(selected_text)
    return result

# Функція для виклику notify-send
def notify_send():
    print(translate())
    command = ["notify-send", "Translater", translate()]
    subprocess.run(command)


# Обробка натиснутих гарячих клавіш і виклик notify-send
def on_press(key):
    try:
        if key in (keyboard.Key.alt, keyboard.Key.shift):
            keys_pressed.add(key)
        if (hasattr(key, 'char') and key.char == 't'):
            keys_pressed.add(key)
            if keyboard.Key.alt in keys_pressed and keyboard.Key.shift in keys_pressed and any(k.char == 't' for k in keys_pressed if hasattr(k, 'char')):
                notify_send()
    except KeyboardInterrupt:
        pass


# Запуск слухача для подій клавіатури
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
