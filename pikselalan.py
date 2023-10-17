import cv2
import numpy as np

# Kamerayı açın
kamera = cv2.VideoCapture(0)  # 0, bilgisayarınızın varsayılan kamera cihazını temsil eder

# Seçilen dört noktayı depolamak için bir liste oluşturun
points = []

while True:
    # Kameradan bir kare yakala
    ret, kare = kamera.read()
    
    # Görüntüyü göster
    cv2.imshow("Kamera Görüntüsü", kare)

    # Fare tıklama olayı için bir işlev tanımlayın
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(kare, (x, y), 5, (0, 0, 255), -1)
            points.append((x, y))
            cv2.imshow('Kamera Görüntüsü', kare)

            # Dört nokta seçildiğinde hesaplama yapın
            if len(points) == 4:
                # Dört noktanın çevresini hesaplayın
                cv2.line(kare, points[0], points[1], (0, 0, 255), 2)
                cv2.line(kare, points[1], points[2], (0, 0, 255), 2)
                cv2.line(kare, points[2], points[3], (0, 0, 255), 2)
                cv2.line(kare, points[3], points[0], (0, 0, 255), 2)

                # Alanı hesaplayın (örnek olarak mutlak değeri kullanarak)
                area = 0.5 * abs((points[0][0]*points[1][1] + points[1][0]*points[2][1] + points[2][0]*points[3][1] + points[3][0]*points[0][1] - points[1][0]*points[0][1] - points[2][0]*points[1][1] - points[3][0]*points[2][1] - points[0][0]*points[3][1]))
                print(f"Seçilen 4 noktaların oluşturduğu alan: {area:.2f} piksel karesi")
                points.clear()  # Noktaları temizle
            
    # Fare tıklama olayını bekleyin
    cv2.setMouseCallback('Kamera Görüntüsü', click_event)
    
    # Q tuşuna basarak döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera ve pencereyi kapat
kamera.release()
cv2.destroyAllWindows()
