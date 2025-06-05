Demo CRUD in Django

Paquetes Instalados (Dentro del entorno virtual)

 django           -- Framework (MVT)
 pillow           -- Archivos
 psycopg2-binary  -- Adapter PostgreSQL
Paso 1: Crear entorno virtual

 python3 -m venv venv
Paso 2: Activar el entorno virtual

 source venv/bin/activate
Paso 3: Instalar paquetes

 pip install -r requirements.txt
Paso 4: Crear un archivo .env para los parametros de la base datos

 DB_NAME= ''
 DB_USER= ''
 DB_PASSWORD= ''
 DB_HOST= ''
 DB_PORT= ''
Paso 5: Ejecutar la aplicación

 python3 manage.py runserver 9090