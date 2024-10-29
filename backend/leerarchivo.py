import xml.etree.ElementTree as ET
from objetos import Empresa, Servicio, Mensaje
from respuesta import generar_xml_resumen,guardar_xml
import globales  # Importar el módulo que contiene las listas globales

def leerarchivo(contenido):
    print('Llegamos a leer archivo')

    try:
        # Leer y parsear el XML desde una cadena
        root = ET.fromstring(contenido)

        # Limpiar listas para evitar duplicados
        globales.empresas.clear()
        globales.mensajes.clear()
        globales.positivos.clear()
        globales.negativos.clear()

        # Cargar palabras positivas y negativas
        for p in root.find('diccionario/sentimientos_positivos').findall('palabra'):
            palabra = p.text.strip().lower()
            globales.positivos.append(palabra)

        for n in root.find('diccionario/sentimientos_negativos').findall('palabra'):
            palabra = n.text.strip().lower()
            globales.negativos.append(palabra)

        # Crear lista de empresas y servicios
        for e in root.find('diccionario/empresas_analizar').findall('empresa'):
            empresa = Empresa(e.find('nombre').text.strip().lower())
            for s in e.find('servicios').findall('servicio'):
                servicio = Servicio(s.get('nombre').strip().lower())
                for a in s.findall('alias'):
                    servicio.agregar_alias(a.text.strip().lower())
                empresa.agregar_servicio(servicio)
            globales.empresas.append(empresa)

        # Crear lista de mensajes
        for m in root.find('lista_mensajes').findall('mensaje'):
            contenido_mensaje = m.text.strip()
            lineas = contenido_mensaje.split('\n')
            if len(lineas) < 4:
                print("Formato de mensaje incorrecto:", contenido_mensaje)
                continue

            try:
                lugar_fecha_str = lineas[0].split(': ')[1].strip()
                lugar, datetime_str = lugar_fecha_str.split(', ')
                fecha, hora = datetime_str.split(' ')
                usuario = lineas[1].split(': ')[1].strip()
                red_social = lineas[2].split(': ')[1].strip()
                texto = lineas[3].strip()
            except (IndexError, ValueError) as e:
                print(f"Error al procesar el mensaje: {contenido_mensaje}")
                print(f"Detalles del error: {e}")
                continue

            mensaje = Mensaje(lugar, fecha, hora, usuario, red_social, texto)
            globales.mensajes.append(mensaje)

        # Llamar a la función de generación XML en respuesta.py
        resumen_xml = generar_xml_resumen()
        guardar_xml(resumen_xml,'resumen.xml')
        return resumen_xml
    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
        raise
    except Exception as e:
        print(f"Error en leerarchivo: {e}")
        raise
