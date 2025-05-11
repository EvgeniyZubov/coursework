import cv2  #Бібліотека OpenCV2
    #BGRTORGB
cap = cv2.VideoCapture(0) # Функція вибору кадрів
if not cap.isOpened():          #Перевірка правильності аргументу вище
    print("Не вдалося відкрити камеру")

while True:
    ret, frame = cap.read()
    if not ret:                 # Перевірка кадру
        print("Не вдалося отримати кадр")
        break

    rgb_color= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Переведення кадру з BGR-простору у RGB
    cv2.imshow("Original", frame)
    cv2.imshow("RGB", rgb_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Очікування кнопки "q" задля вимкнення камери власноруч
        break

cap.release()
cv2.destroyAllWindows()
