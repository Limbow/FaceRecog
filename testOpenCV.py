#Esta app te abrirá una ventana donde detectara de forma automatica los rostros
#Lo use para testar las bibliotecas y profundizar mis conocimientos en este campo


import face_recognition
import cv2


video_capture = cv2.VideoCapture(0)  # Si DroidCam no funciona, prueba con índices 1 o 2

print("Presiona 'q' para salir.")

while True:

    ret, frame = video_capture.read()
    if not ret:
        print("No se pudo acceder a la cámara.")
        break


    rgb_frame = frame[:, :, ::-1]


    face_locations = face_recognition.face_locations(rgb_frame)


    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


    cv2.imshow("Reconocimiento Facial - Presiona 'q' para salir", frame)

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
