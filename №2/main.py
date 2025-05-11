import cv2  #Бібліотека OpenCV2

    #  ВІДЕОЗОБРАЖЕННЯ
#Ініціалізація камери
cap = cv2.VideoCapture("video1.mp4")

#Перевірка роботи камери
if not cap.isOpened():
    print("Не вдалося відкрити відеофайл")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не вдалося отримати кадр")
        break
    cv2.waitKey(2) # Затримка читання кадрів задля нормальної швидкості відеозображення
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):       #Очікування кнопки "x" задля вимкнення відеозображення власноруч
        break

cap.release()
cv2.destroyAllWindows()

    #  ВІДЕОКАМЕРА
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не вдалося відкрити камеру")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не вдалося отримати кадр")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Очікування кнопки "q" задля вимкнення камери власноруч
        break

cap.release()
cv2.destroyAllWindows()
