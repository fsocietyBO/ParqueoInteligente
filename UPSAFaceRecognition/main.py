import cv2
from simple_facerec import SimpleFacerec

if __name__ == '__main__':
    # Codificar imagenes de una carpeta

    sfr = SimpleFacerec()
    sfr.load_encoding_images("Caras/")

    # Abrir camara
    cap = cv2.VideoCapture("rtsp://192.168.67.251:8080/h264_ulaw.sdp")
    # cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detectar caras
        localizacion_cara, nombre_cara = sfr.detect_known_faces(frame)
        for loc_cara, nombre in zip(localizacion_cara, nombre_cara):
            print(loc_cara)
            # arriba, izquierda, abajo, derecha = loc_cara[0], loc_cara[1], loc_cara[2], loc_cara[3]
            y1, x2, y2, x1 = loc_cara[0], loc_cara[1], loc_cara[2], loc_cara[3]

            cv2.putText(frame, nombre , (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()