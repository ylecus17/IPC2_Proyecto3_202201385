from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from leerarchivo import leerarchivo

app = Flask(__name__)
CORS(app)  # Permitir CORS desde cualquier origen

@app.route('/api/cargar', methods=['POST'])
def cargar():
    print('Llegó una solicitud a Flask')

    # Verificar si se envió un archivo con el nombre 'archivo'
    if 'archivo' not in request.files:
        return jsonify({'mensaje': 'No se envió ningún archivo'}), 400

    archivo = request.files['archivo']

    try:
        # Leer el contenido del archivo
        contenido = archivo.read().decode('utf-8')  # Leer y decodificar el archivo como texto UTF-8
        
        # Imprimir el contenido del archivo en la consola
        print(f"Contenido del archivo XML:\n{contenido}")
        leerarchivo(contenido)
        # Devolver el contenido del archivo en la respuesta, manteniendo el formato XML
        return Response(contenido, mimetype='application/xml'), 200

    except Exception as e:
        # Manejo de errores en caso de fallo al leer o procesar el archivo
        print(f"Error al procesar el archivo: {e}")
        return jsonify({'mensaje': 'Error al procesar el archivo'}), 500

if __name__ == '__main__':
    app.run(debug=True)

