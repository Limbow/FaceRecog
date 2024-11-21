**Quiero aclarar que el archivo app.py es la version web y el archivo testOpenCV.py es la version escritorio**
Ante cualquier duda o problema no duden en contactarme: joacovasquez0@gmail.com

Proyecto de Reconocimiento Facial en Flask

Este proyecto implementa una aplicación web utilizando Flask que permite registrar rostros, almacenar imágenes de los mismos y realizar la detección y comparación de rostros en tiempo real a través de la cámara. Está basado en la librería face_recognition para la detección y comparación de rostros.

Requisitos
Asegúrate de tener los siguientes requisitos previos instalados:

Python 3.x (se recomienda usar la versión 3.7 o superior).
pip (gestor de paquetes de Python).
CMake (se necesita para compilar algunas dependencias de dlib).

Instalación de CMake (Si es necesario)
Si no tienes CMake instalado, puedes descargarlo desde su página oficial, o instalarlo usando el siguiente comando si estás en un sistema basado en Linux:

"sudo apt-get install cmake" *sin las comillas*

En sistemas Windows, puedes instalar CMake mediante el instalador de Windows.

Instalación de Dependencias

pip install flask
pip install opencv-python
pip install face_recognition
pip install dlib

Ejecutar el Proyecto
Inicia el servidor Flask:

Para ejecutar la aplicación, abre una terminal, navega al directorio del proyecto y ejecuta:

Desde el CMD: *python app.py*
Esto iniciará el servidor Flask en http://0.0.0.0:5000/. Podrás acceder a la aplicación desde cualquier navegador web. http://localhost:5000

Ahí podrás ver la interfaz de la transmisión en vivo de la cámara y un formulario para registrar rostros.

Registrar un rostro:

Asegúrate de estar bien iluminado y bien enfocado frente a la cámara.
En la página, ingresa un nombre para el rostro que deseas registrar.
La aplicación tomará una foto, la recortará y la guardará en una carpeta llamada known_faces con el nombre ingresado.
Detección de Rostros:

En la misma interfaz, mientras el servidor esté en ejecución, se detectarán y etiquetarán los rostros detectados en tiempo real.



Estructura del Proyecto
El proyecto está compuesto por los siguientes archivos:

app.py: Archivo principal con la lógica de la aplicación Flask, la captura de imágenes desde la cámara, el registro de rostros y la detección de rostros en tiempo real.
known_faces/: Carpeta donde se guardan las imágenes de los rostros registrados.


Notas Adicionales
Cámara: El proyecto utiliza la cámara predeterminada de tu computadora o una cámara externa conectada. Si deseas usar una cámara diferente o configurar DroidCam, asegúrate de que el dispositivo esté configurado correctamente.

Base de datos (Opcional): Actualmente, el sistema utiliza una lista en memoria para almacenar las codificaciones y los nombres de los rostros registrados. Puedes modificarlo fácilmente para almacenar esta información en una base de datos como MySQL, SQLite, o MongoDB si prefieres mantener los rostros registrados entre reinicios del servidor.

Solución de Problemas
Si encuentras errores al instalar las dependencias, asegúrate de tener las versiones correctas de Python y las librerías necesarias. En caso de que dlib o face_recognition no se instalen correctamente, a mi me funciono el siguiente comando *pip install setuptools*

Te recomiendo que si aun sigue sin funcionar revises bien la documentacion necesaria


