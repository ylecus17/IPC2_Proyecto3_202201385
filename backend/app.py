from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from leerarchivo import leerarchivo
from respuesta import filtrar_por_fecha,filtrar_por_fecha_y_empresa,guardar_xml

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

        # Procesar el contenido del archivo (llama a tu función aquí)
        leerarchivo(contenido)

        # Devolver el contenido del archivo en formato XML
        return jsonify({
            'mensaje': 'Archivo procesado correctamente',
            'contenido_archivo': contenido
        }), 200

    except Exception as e:
        # Manejo de errores en caso de fallo al leer o procesar el archivo
        print(f"Error al procesar el archivo: {e}")
        return jsonify({'mensaje': 'Error al procesar el archivo'}), 500

@app.route('/api/resumen', methods=['GET'])
def obtener_resumen():
    try:
        with open('resumen.xml', 'r', encoding='utf-8') as f:
            contenido = f.read()
        return Response(contenido, mimetype='application/xml'), 200
    except FileNotFoundError:
        return jsonify({'mensaje': 'El archivo resumen no fue encontrado'}), 404
    except Exception as e:
        print(f"Error al leer el archivo resumen: {e}")
        return jsonify({'mensaje': 'Error al leer el archivo resumen'}), 500


@app.route('/api/filtrar_resumen', methods=['POST'])
def filtrar_resumen():
    # Obtener valores de fecha y empresa desde el formulario
    fecha = request.form.get('fecha')
    empresa = request.form.get('empresa')
    
    # Verificar qué datos llegan al backend
    print("Fecha recibida:", fecha)
    print("Empresa recibida:", empresa)
    
    # Verificar que la fecha esté presente
    if not fecha:
        print("Error: La fecha es requerida")
        return jsonify({"error": "La fecha es requerida"}), 400
    
    try:
        # Filtrado solo por fecha
        if not empresa:
            print("Realizando filtrado solo por fecha")
            resultados = filtrar_por_fecha(fecha)
            if resultados is None:
                return jsonify({"error": "No se encontraron resultados para la fecha especificada."}), 404
            
            guardar_xml(resultados, "fecha_filter.xml")
        
        # Filtrado por fecha y empresa
        else:
            print("Realizando filtrado por fecha y empresa")
            resultados = filtrar_por_fecha_y_empresa(fecha, empresa)
            
            if resultados is None:
                return jsonify({"error": "No se encontraron resultados para la fecha y empresa especificadas."}), 404
            guardar_xml(resultados, "fecha_filter.xml")
    except Exception as e:
        print(f"Error en la función de filtrado: {e}")
        return jsonify({"error": "Se encontró un error al procesar la solicitud."}), 500
    
    # Responder con éxito
    return jsonify({"mensaje": "Archivo filtrado creado correctamente."}), 200

@app.route('/api/fecha_filter', methods=['GET'])
def obtener_ff():
    try:
        with open('fecha_filter.xml', 'r', encoding='utf-8') as f:
            contenido = f.read()
        return Response(contenido, mimetype='application/xml'), 200
    except FileNotFoundError:
        return jsonify({'mensaje': 'El archivo resumen no fue encontrado'}), 404
    except Exception as e:
        print(f"Error al leer el archivo resumen: {e}")
        return jsonify({'mensaje': 'Error al leer el archivo resumen'}), 500

if __name__ == '__main__':
    app.run(debug=True)
