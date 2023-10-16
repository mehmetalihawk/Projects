import cv2
import numpy as np
#import serial
import time

#ser=serial.Serial('/dev/ttyACM0',9600)
#hscr04=[]
# Kamera kaynağını belirle (0 sa bilgisayar kamerası, 1 ise harici kamera)
cap = cv2.VideoCapture(0)

# Görüntü boyutunu belirle
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height, sep=" ")

# 7x7 dikdörtgenlerin boyutunu ve konumlarını belirle
rect_width = int(width / 12)
rect_height = int(height / 12)
rects = []
for i in range(12):
    for j in range(12):
        rect = (j * rect_width, i * rect_height, rect_width, rect_height)
        rects.append(rect)

# Şerit takip algoritması
while True:
    ret, frame = cap.read()  # Kameradan görüntü oku

    black_ratios = []  # Görüntüyü parçalara ayır ve her bir parçadaki siyah piksel oranını hesapla

    for rect in rects:
        x, y, w, h = rect
        sub_frame = frame[y:y + h, x:x + w]
        black_pixels = cv2.countNonZero(cv2.inRange(sub_frame, np.array([0, 0, 0]), np.array([50, 50, 50])))
        ratio = black_pixels / (w * h)  # Siyah piksel yüzdesini hesapla ve listeye ekle
        black_ratios.append(round(ratio * 100))
        cv2.putText(frame, f'{black_ratios[-1]}%', (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # Siyah piksel yüzdelerini 7x7 matris şeklinde yazdır
    matrix = np.array(black_ratios).reshape((12, 12))

    # Her bir elemanı 40'tan küçükse 0, 40 veya daha büyükse 1 olarak değiştir
    matrix = np.where(matrix < 40, 0, 1)

    # Şerit takip algoritması
    center_x = width // 2
    distances = [i - center_x for i in np.where(matrix[6] == 1)[0]]
    if not distances:
        print('Şerit bulunamadı!')
    else:
        avg_distance = sum(distances) / len(distances)
        avg_distance+=314
        data=avg_distance + 0.5
        print(f'Orta çizgiden {avg_distance:.2f} piksel {"" if avg_distance > 0 else "sola "}kayıldı.')
        if avg_distance < -0.5:
            print('Sola dön.')
        elif avg_distance > 0.5:
            print('Sağa dön.')

    cv2.imshow('frame', frame)  # Görüntüyü ekrana göster
    

    #SendSerialPort

#    ser.write(data.encode('utf-8'))


    #ReceiverSerialPort

#    if ser.in_waiting > 0:

#        for i in range(0,4):
#            hscr04[i]=int(ser.readline().decode('utf-8'))
#            print(hscr04[i])

#        kizil = bool(ser.readline().decode('utf-8'))

#        sicaklik=float(ser.readline().decode('utf-8'))

#        dumandeger=float(ser.readline().decode('utf-8'))

 #       print(kizil,sicaklik,dumandeger,sep="\n")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()