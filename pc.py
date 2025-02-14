import cv2
import numpy as np
import pyautogui
import requests
import time

IP = "0.0.0.0"
vps_url = f'http://{IP}:5000/update_frame'  # Замените на IP вашего VPS

while True:
    # Захватываем изображение экрана
    img = pyautogui.screenshot()

    # Преобразуем изображение в массив NumPy
    frame = np.array(img)

    # Преобразуем цветовую схему из RGB в BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Отправляем изображение на VPS
    _, buffer = cv2.imencode('.jpg', frame)
    response = requests.post(vps_url, data=buffer.tobytes())

    if response.status_code == 204:
        print("Frame sent successfully")
    else:
        print("Failed to send frame")

    time.sleep(0.1)  # Задержка для снижения нагрузки
