# Aplicación web Flask para acceder a las APIs del INE (Instituto Nacional de Estadística)
# sobre tasas de paro. Proporciona una interfaz web para consultar estadísticas
# de desempleo españolas a través de distintos endpoints de API.
from flask import Flask, render_template, request, jsonify
import requests
import json
import os

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de las APIs del INE para tasas de paro
# Cada API representa una fuente de datos de desempleo con parámetros específicos
INE_APIS = [
    {
        "id": "api1",
        "name": "Tasa de paro general",
        "description": "Obtiene la tasa de paro general del mercado laboral",
        "endpoint": "https://api.ine.es/empleo/paro/general",
        "parameters": [
            {"name": "ano", "type": "number", "required": True, "label": "Año"},
            {"name": "sexo", "type": "select", "required": False, "label": "Sexo", "options": ["Total", "Hombres", "Mujeres"]}
        ]
    },
    {
        "id": "api2",
        "name": "Tasa de paro por edad",
        "description": "Obtiene la tasa de paro desglosada por grupos de edad",
        "endpoint": "https://api.ine.es/empleo/paro/edad",
        "parameters": [
            {"name": "ano", "type": "number", "required": True, "label": "Año"},
            {"name": "grupo_edad", "type": "select", "required": False, "label": "Grupo de edad", "options": ["16-24", "25-34", "35-44", "45-54", "55+"]}
        ]
    },
    {
        "id": "api3",
        "name": "Tasa de paro por comunidad autónoma",
        "description": "Obtiene la tasa de paro por región geográfica",
        "endpoint": "https://api.ine.es/empleo/paro/comunidad",
        "parameters": [
            {"name": "ano", "type": "number", "required": True, "label": "Año"},
            {"name": "comunidad", "type": "select", "required": False, "label": "Comunidad Autónoma", "options": ["Andalucía", "Aragón", "Asturias", "Baleares", "Canarias", "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña", "Comunidad Valenciana", "Extremadura", "Galicia", "Madrid", "Murcia", "Navarra", "País Vasco", "Rioja"]}
        ]
    }
]

# Ruta de la página principal
# Muestra una lista de las APIs del INE disponibles para que el usuario las seleccione y consulte
@app.route('/')
def index():
    """Página principal con las opciones de APIs"""
    return render_template('index.html', apis=INE_APIS)

# Ruta para mostrar los detalles de una API
# Muestra información sobre una API específica, incluyendo su descripción y parámetros
@app.route('/api/<api_id>')
def api_detail(api_id):
    """Página de detalles de una API específica"""
    # Busca la API por su ID en la lista INE_APIS
    api = next((a for a in INE_APIS if a["id"] == api_id), None)
    if not api:
        return jsonify({"error": "API no encontrada"}), 404
    return render_template('api_detail.html', api=api)

# Ruta para ejecutar llamadas a la API
# Recibe peticiones POST con parámetros y ejecuta la API seleccionada
@app.route('/api/<api_id>/execute', methods=['POST'])
def execute_api(api_id):
    """Ejecuta la API seleccionada con los parámetros proporcionados"""
    # Busca la API por su ID
    api = next((a for a in INE_APIS if a["id"] == api_id), None)
    if not api:
        return jsonify({"error": "API no encontrada"}), 404
    
    # Extrae los parámetros de los datos del formulario
    params = {}
    for param in api["parameters"]:
        value = request.form.get(param["name"])
        if value:
            params[param["name"]] = value
    
    try:
        # Ejecuta la llamada a la API con los parámetros proporcionados
        response = requests.get(api["endpoint"], params=params, timeout=30)
        data = response.json()
        return jsonify({
            "success": True,
            "data": data,
            "params": params
        })
    except Exception as e:
        # Maneja cualquier error que ocurra durante la llamada a la API
        return jsonify({
            "success": False,
            "error": str(e)
        })

# Ruta para restablecer los parámetros de una API
# Devuelve un mensaje de éxito indicando que los parámetros han sido restablecidos
@app.route('/reset/<api_id>')
def reset_api(api_id):
    """Resetea los parámetros de una API"""
    return jsonify({"success": True, "message": "Parámetros reseteados"})

# Punto de entrada principal de la aplicación
# Inicia el servidor de desarrollo de Flask cuando el script se ejecuta directamente.
# En producción se usa Gunicorn (inicioINE:app); este bloque solo aplica al
# desarrollo local y respeta la variable de entorno PORT.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host='0.0.0.0', port=port)
