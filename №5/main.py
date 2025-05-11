import cv2  #Бібліотека OpenCV2
import numpy as np

    #Виділення меж Prewitt
cap = cv2.VideoCapture(0) # Функція вибору кадрів
if not cap.isOpened():          #Перевірка правильності аргументу вище
    print("Не вдалося відкрити камеру")

    #Ядра Prewitt
core_px = np.array([
    [-1,0,1],
    [-1,0,1],
    [-1,0,1]
],dtype=np.float32)

core_py = np.array([
    [1,1,1],
    [0,0,0],
    [-1,-1,-1]
],dtype=np.float32)

T = int(input("Введіть поріг яркості зображення(0-255): "))
if T > 255 or T < 0:
    print("T не може бути вище за 255 або нижче за 0, встановлено 1 за замовчуванням. ")
    T = 1

while True:
    ret, frame = cap.read()
    if not ret:                 # Перевірка кадру
        print("Не вдалося отримати кадр")
        break
    #Переведення кадру у GRAY-простір
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Градієнти
    grad_x = cv2.filter2D(gray, ddepth=cv2.CV_32F, kernel=core_px)
    grad_y = cv2.filter2D(gray, ddepth=cv2.CV_32F, kernel=core_py)

    #Суміщення по градієнтах(утворюємо одну картинку)
    magnitude = cv2.magnitude(grad_x, grad_y)

    #Приводимо картинку до вигляду, у якому можно її подивитися(нормалізуємо та переводимо у 8бітне зображення)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    magnitude = magnitude.astype(np.uint8)

    _, edge_binary = cv2.threshold(
        magnitude,
        T,
        255,
        cv2.THRESH_BINARY
    )

    cv2.imshow("Original", frame)
    cv2.imshow('Magnitude', magnitude)
    cv2.imshow('Binary Prewitt', edge_binary)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Очікування кнопки "q" задля вимкнення камери власноруч
        break

cap.release()
cv2.destroyAllWindows()
