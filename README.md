
# Programador de Publicaciones y Videos

Este es un código que permite programar publicaciones y videos para subirlos en redes sociales o plataformas de videos en el momento deseado. Consiste en tres archivos de Python:

## Archivos

- [db.py](https://github.com/Overdjosed/reddit/blob/master/reddit_scheduler/db.py): Este archivo contiene la base de datos y se encarga de guardar toda la información ingresada a través del GUI. Almacena usuarios, subreddits, archivos y publicaciones programadas.
- [gui.py](https://github.com/Overdjosed/reddit/blob/master/reddit_scheduler/gui.py): Permite interactuar con la base de datos, permitiendo agregar o eliminar usuarios, posts o subreddits. También facilita la programación de publicaciones y videos, especificando si serán NSFW (Not Safe For Work) o no. Además, permite proporcionar una URL de salida (opcional).
- [tasks_admin.py](https://github.com/Overdjosed/reddit/blob/master/reddit_scheduler/tasks_admin.py): Este código se ejecutará automáticamente cada hora para subir los posts sin interacción del usuario. En sistemas Windows, deberá configurarse en el Administrador de tareas (Task Scheduler), mientras que en sistemas Linux, se proporcionará un programa para instalar el Administrador de tareas.

## Instalación y Configuración

Para instalar la tarea programada en el Administrador de tareas de Windows, sigue estos pasos:

1. Abre el Administrador de tareas: Puedes encontrarlo en el menú Inicio escribiendo "Task Scheduler" o "Administrador de tareas" en la barra de búsqueda.
2. En el panel derecho, selecciona "Crear tarea básica...".
3. Proporciona un nombre y una descripción para la tarea y haz clic en "Siguiente".
4. Selecciona "Diariamente" como la frecuencia y haz clic en "Siguiente".
5. Establece la hora y la repetición cada 1 hora durante un día. Haz clic en "Siguiente".
6. Selecciona "Iniciar un programa" y proporciona la ruta completa del ejecutable de Python (python.exe). En el campo "Agregar argumentos (opcional)", especifica la ruta completa de tasks_admin.exe.
7. Haz clic en "Siguiente" y luego en "Finalizar" para crear la tarea programada.

## Uso

<img width="913" alt="image" src="https://github.com/Overdjosed/reddit_post_scheduler/assets/114219289/c937289f-418a-419f-9bd4-9231fdd676a4">



Ejecuta el archivo [gui.exe](https://github.com/Overdjosed/reddit/blob/master/reddit_scheduler/gui.py) para interactuar con el programa. En el apartado "Users", introduce tu nombre de usuario y contraseña de Reddit reales. Los otros parámetros se usarán por defecto.

Podrás agregar o eliminar usuarios, posts o subreddits utilizando las opciones disponibles en el GUI.

<img width="917" alt="image" src="https://github.com/Overdjosed/reddit_post_scheduler/assets/114219289/a19eaefa-aaf4-4b35-9830-bbd6ddebbfb7">


Para programar una publicación o un video, especifica el contenido, fecha/hora, plataforma y si será NSFW o no. La URL de salida es opcional.

La subida de archivos tendrá una variación máxima de 1 hora a la hora especificada.


<img width="915" alt="image" src="https://github.com/Overdjosed/reddit_post_scheduler/assets/114219289/ca112352-67d1-43ed-86c0-6273b6451519">


Nota importante: Reddit solo admite un video a la vez, por lo que solo podrás subir un video junto con las imágenes que desees, pero no podrás subir más de un video. Sin embargo, podrás subir tantas imágenes como desees.

Con estos pasos, podrás utilizar el programador para automatizar tus publicaciones y videos en Reddit de manera efectiva. Recuerda revisar las políticas y términos de servicio de Reddit para asegurarte de cumplir con sus reglas y evitar problemas con tu cuenta.

Post_scheduler v2.0
