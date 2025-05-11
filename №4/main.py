import cv2  #Бібліотека OpenCV2
import numpy as np

    #Вертикальний зсув
cap = cv2.VideoCapture(0) # Функція вибору кадрів
if not cap.isOpened():          #Перевірка правильності аргументу вище
    print("Не вдалося відкрити камеру")

dy = float(input("Введіть dy (-y = вгору, y = вниз): "))

while True:
    ret, frame = cap.read()
    if not ret:                 # Перевірка кадру
        print("Не вдалося отримати кадр")
        break

    M = np.float32([[1, 0, 0], [0, 1, dy]])

    shift_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

    cv2.imshow("Original", frame)
    cv2.imshow("RGB", shift_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Очікування кнопки "q" задля вимкнення камери власноруч
        break

cap.release()
cv2.destroyAllWindows()
