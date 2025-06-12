# SNAKE DEMO DJANGO
### CRUD 
###### Paquetes Instalados (Dentro del entorno virtual)
- Docker 28.2.2
- Pyhon 3.12.3
- Django
- virtualenv

#### 1.- Clonar el repositorio

Utiliza `git clone` para clonar.

    git clone [URL_DEL_REPOSITORIO]
    cd [NOMBRE_DEL_PROYECTO]
    
#### 2.- Configurar entorno virtual

    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate  # Windows

#### 3. Instalar dependencias　

	pip install -r requirements.txt

###### archivo requirements.txt

```asgiref==3.8.1
Django==5.2.2
et_xmlfile==2.0.0
openpyxl==3.1.5
pillow==11.2.1
psycopg2-binary==2.9.10
python-decouple==3.8
sqlparse==0.5.3

```
#### 4. Configurar variables de entorno
###### Crea un archivo .env en la raíz del proyecto con:

```
SECRET_KEY=tu_clave_secreta_aqui
DB_NAME=nombre_bd
DB_USER=usuario_bd
DB_PASSWORD=contraseña_bd
DB_HOST=localhost
DB_PORT=5432
```

#### 5. Configurar base de datos
- Crear la base de datos en PostgreSQL
- Configurar en programas/settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config ('DB_NAME'),
        'USER': config ('DB_USER'),
        'PASSWORD': config ('DB_PASSWORD'),
        'HOST': config ('DB_HOST'),
        'PORT': config ('DB_PORT')
    }
}
```
____
# CREAR BASE DE DATOS EN POSTGRESQL DOCKER
###### El comando se utiliza para descargar e instalar Docker en tu sistema de manera automatizada.

	curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh

#### 1.- Comando para crear un contenedor Docker con PostgreSQL.

	sudo docker run --name pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=snake -d postgres:17

#### 2.- Para conectar Django con esta base de datos PostgreSQL:
1. Primero instala el adaptador PostgreSQL para Python:

```
pip install psycopg2-binary
```
#### 3.- Comandos útiles para gestionar el contenedor:

- Verificar que el contenedor está corriendo:
```
docker ps
```
###### ejemplo:
- docker ps

| CONTAINER ID  | IMAGE  | COMMAND  | CREATED  | STATUS  | PORTS  | NAMES  |
| :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: |
| 646e724c67a5  | postgres:17  | "docker-entrypoint.s…"  | 5 days ago  | Up 25 hours  | 5432/tcp  | pg  |


- Detener el contenedor:
```
docker stop pg
```
- Iniciar el contenedor nuevamente:
```
docker start pg
```
- Acceder a la consola de PostgreSQL dentro del contenedor:
```
docker exec -it pg psql -U postgres -d snake
```

## CREAR TABLAS EN LA BASE DE DATOS
1. Tabla "profile"
```
snake=#
CREATE TABLE profile(
id serial primary key, 
username varchar(50), 
name varchar(50), 
phone int, 
email varchar(50), 
photo varchar(50));
```
- Agregar nueva columna a la tabla "profile".
```
ALTER TABLE profile ADD COLUMN id_user INT;
```

2.- Crear tabla llamada "bitacora".
```
CREATE TABLE bitacora(
id serial primery key,
movimiento varchar(50), 
fecha timestamp);
```
- Agregar nueva columna a la tabla "bitacora" llamada "usuario".
```
ALTER TABLE bitacora ADD COLUMN usuario INT;
```

4.- Crear tabla llamada tareas.
```
CREATE TABLE tareas (
id serial primary key, 
nombre  varchar(50), 
descripcion varchar(100), 
estatus boolean, 
id_profile int, 
foreign key(id_profile) references profile(id));

```

3.- Crear una Claves Foráneas.
- profile
```
ALTER TABLE profile ADD FOREIGN KEY(id_user) REFERENCES auth_user(id);
```
- bitacora
```
ALTER TABLE bitacora ADD FOREIGN KEY(usuario) REFERENCES auth_user(id);
```

## Ejecutar la aplicación

```
 python3 manage.py runserver 

```
# NOTA
#### Si hay errores de migración:
```
python manage.py makemigrations
python manage.py migrate
```





