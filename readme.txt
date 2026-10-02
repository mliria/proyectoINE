PROYECTO INE - INSTRUCCIONES DE ARRANQUE
===========================================

Aplicación web Flask para consultar tasas de paro del INE mediante APIs.


REQUISITOS PREVIOS
------------------

- Python 3.7 o superior instalado
- pip (gestor de paquetes de Python)
- Conexión a internet


PASOS PARA ARRANCAR LA APLICACIÓN
---------------------------------

1. Abrir una terminal en la carpeta del proyecto:
   cd /home/marcos/proyectos/proyectoINE

2. Crear y activar un entorno virtual (si no existe):
   python3 -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows

3. Instalar las dependencias del requirements.txt:
   pip install -r requirements.txt

4. Ejecutar la aplicación Flask:
   python inicioINE.py

5. La aplicación se ejecutará en:
   http://0.0.0.0:5000

   Puedes acceder desde el navegador usando:
   http://localhost:5000


PARAR LA APLICACIÓN
-------------------

En la terminal donde se está ejecutando, presiona:
Ctrl + C


DESCRIPCIÓN DE LA APLICACIÓN
----------------------------

La aplicación muestra tres APIs del INE para consultar tasas de paro:

- API 1: Tasa de paro general (por año y sexo)
- API 2: Tasa de paro por edad (por año y grupo de edad)
- API 3: Tasa de paro por comunidad autónoma (por año y región)

Cada API tiene su propia página de detalles donde se pueden introducir
parámetros y ejecutar la consulta.


DOCKER / CLOUD DEPLOYMENT
=========================

La aplicación se puede empaquetar en un contenedor Docker y desplegar en
cualquier PaaS portable (Render, Railway, Fly.io). El contenedor usa Gunicorn
como servidor WSGI de producción y escucha en el puerto indicado por la
variable de entorno PORT (que la plataforma inyecta automáticamente).

Comando de arranque (Gunicorn):

   gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 inicioINE:app

Ruta de importación de la aplicación: inicioINE:app


CONSTRUIR LA IMAGEN LOCALMENTE
------------------------------

   docker build -t proyectoine .


EJECUTAR EL CONTENEDOR LOCALMENTE
---------------------------------

   docker run -p 8000:8000 -e PORT=8000 proyectoine

Después abre http://localhost:8000 en el navegador.

Alternativa con Docker Compose (paridad local):

   docker compose up --build


DESPLEGAR EN RENDER
-------------------

1. Sube el repositorio a GitHub/GitLab.
2. En Render, crea un nuevo "Web Service" y conecta el repositorio.
3. Render detecta render.yaml (env: docker) y construye con el Dockerfile.
4. Render inyecta la variable PORT; no es necesario configurarla.
5. El health check apunta a la ruta "/".


DESPLEGAR EN RAILWAY
--------------------

1. Sube el repositorio a GitHub.
2. En Railway, crea un nuevo proyecto y elige "Deploy from GitHub repo".
3. Railway detecta el Dockerfile y construye la imagen automáticamente.
4. Railway inyecta la variable PORT; el Procfile/Dockerfile la respetan.
5. Genera un dominio público en la pestaña Settings > Networking.


DESPLEGAR EN FLY.IO
-------------------

1. Instala flyctl y ejecuta: fly launch
2. Acepta el Dockerfile detectado (no generes uno nuevo).
3. Asegúrate de que la app escucha en 0.0.0.0 y en el puerto de $PORT.
4. Ejecuta: fly deploy
5. Fly.io inyecta PORT; el contenedor se enlaza a él automáticamente.


NOTAS
-----

- No se requieren secretos ni variables de entorno obligatorias.
- El puerto 8000 es solo un valor por defecto; la plataforma puede
  sobrescribirlo mediante PORT.
- Para desarrollo local: python inicioINE.py (usa PORT o 5000 por defecto).
  Activa el modo debug con FLASK_DEBUG=1.