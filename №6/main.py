import cv2  #Бібліотека OpenCV2
import numpy as np

cap = cv2.VideoCapture(0) # Функція отримання кадрів

def nothing(x):
    pass

cv2.namedWindow("HF Filter")
cv2.createTrackbar("Threshold", "HF Filter", 10, 255, nothing) #Створення віджета повзунка порогу
cv2.createTrackbar("Center", "HF Filter", 8, 50, nothing)    #Створення віджета повзунка центрального числа
cv2.createTrackbar("Edge", "HF Filter", 1, 10, nothing)     #Створення віджета повзунка крайнього числа

if not cap.isOpened():          #Перевірка правильності аргументу вище
    print("Не вдалося відкрити камеру")

while True:
    ret, frame = cap.read()
    if not ret:                 # Перевірка кадру
        print("Не вдалося отримати кадр")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Перетворення у градації сірого

    cv2.imshow("Original", frame)


    thresh_value = cv2.getTrackbarPos("Threshold", "HF Filter")  #Отримання значення порогу
    center_val = cv2.getTrackbarPos("Center", "HF Filter")      #Отримання значення центрального числа ядра
    edge_val = cv2.getTrackbarPos("Edge", "HF Filter")         #Отримання значення крайнього числа ядра

    kernel = np.array([[-edge_val, -edge_val, -edge_val],           #Ядро фільтра ВЧ
                       [-edge_val, center_val, -edge_val],
                       [-edge_val, -edge_val, -edge_val]])

    high_pass = cv2.filter2D(gray, -1, kernel)    #Інвертування кольорів для відображення вищих частот

    _, thresholded = cv2.threshold(high_pass, thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imshow("HF Filter", thresholded)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Очікування кнопки "q" задля вимкнення камери власноруч
        break

cap.release()
cv2.destroyAllWindows()
