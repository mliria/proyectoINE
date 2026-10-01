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