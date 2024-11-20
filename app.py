from flask import Flask, Response, request
import cv2
import face_recognition
import os

app = Flask(__name__)

# Configurar la cámara (usando DroidCam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Lista para almacenar encodings y nombres
known_face_encodings = []
known_face_names = []

def load_known_faces():
    known_faces_dir = "known_faces"
    if os.path.exists(known_faces_dir):
        for filename in os.listdir(known_faces_dir):
            if filename.endswith(".jpg"):
                image_path = os.path.join(known_faces_dir, filename)
                image = cv2.imread(image_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_image)
                if face_locations:
                    face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(filename.split(".")[0])  # Usar el nombre del archivo como nombre

# Llamar a la función para cargar los rostros conocidos al iniciar el servidor
load_known_faces()


def register_face(frame, name):
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros en la imagen
    face_locations = face_recognition.face_locations(rgb_frame)
    if not face_locations:
        raise ValueError("No se detectó ningún rostro en la imagen.")

    # Obtener las codificaciones de los rostros
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if not face_encodings:
        raise ValueError("No se pudo generar la codificación del rostro.")


    known_face_encodings.append(face_encodings[0])
    known_face_names.append(name)

    # Guardar la imagen del rostro
    save_path = "known_faces"
    os.makedirs(save_path, exist_ok=True)  # Crear la carpeta si no existe

    # Recortar la imagen para el rostro detectado
    top, right, bottom, left = face_locations[0]
    face_image = frame[top:bottom, left:right]
    image_path = os.path.join(save_path, f"{name}.jpg")
    cv2.imwrite(image_path, face_image)
    print(f"Rostro de {name} guardado en {image_path}.")


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detectar los rostros en el frame
            face_locations = face_recognition.face_locations(rgb_frame, model='hog')

            
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Comparar el rostro detectado con los rostros registrados
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Desconocido"

                    # Si hay una coincidencia, asignar el nombre registrado
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    # Dibujar un rectángulo alrededor del rostro detectado
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Codificar el frame en formato JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Generar un flujo de datos compatible con MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registro y Detección de Rostros</title>
    </head>
    <body>
        <h1>Transmisión en Vivo con Registro de Rostros</h1>
        <img src="/video_feed" alt="Transmisión en Vivo">
        <form action="/register" method="post">
            <label for="name">Nombre:</label>
            <input type="text" id="name" name="name" required>
            <button type="submit">Registrar Rostro</button>
        </form>
    </body>
    </html>
    '''


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')

    success, frame = cap.read()
    if not success:
        return '<h1>Error al capturar la imagen</h1><a href="/">Volver</a>'

    try:
        register_face(frame, name)
        return f'<h1>Rostro de "{name}" registrado con éxito</h1><a href="/">Volver</a>'
    except ValueError as e:
        return f'<h1>Error: {e}</h1><a href="/">Volver</a>'


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
