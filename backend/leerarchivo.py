import xml.etree.ElementTree as ET
from objetos import Empresa, Servicio, Mensaje, Diccionario

def leerarchivo(contenido):
    print('Llegamos a leer archivo')
    try:
        # Leer y parsear el XML desde una cadena
        root = ET.fromstring(contenido)

        # Crear diccionario para sentimientos
        diccionario = Diccionario()
        for p in root.find('diccionario/sentimientos_positivos').findall('palabra'):
            diccionario.agregar_positivo(p.text.strip().lower())
        for n in root.find('diccionario/sentimientos_negativos').findall('palabra'):
            diccionario.agregar_negativo(n.text.strip().lower())

        # Crear lista de empresas y servicios
        empresas = []
        for e in root.find('diccionario/empresas_analizar').findall('empresa'):
            empresa = Empresa(e.find('nombre').text.strip().lower())

            for s in e.find('servicios').findall('servicio'):
                servicio = Servicio(s.get('nombre').strip().lower())
                for a in s.findall('alias'):
                    servicio.agregar_alias(a.text.strip().lower())
                empresa.agregar_servicio(servicio)

            empresas.append(empresa)

        # Crear lista de mensajes
        mensajes = []
        for m in root.find('lista_mensajes').findall('mensaje'):
            # Separar las propiedades dentro del contenido del mensaje
            contenido_mensaje = m.text.strip()
            lineas = contenido_mensaje.split('\n')
            lugar_fecha = lineas[0].split(': ')[1].strip()
            usuario = lineas[1].split(': ')[1].strip()
            red_social = lineas[2].split(': ')[1].strip()
            texto = lineas[3].strip()

            # Dividir lugar y fecha
            lugar, fecha_hora = lugar_fecha.split(', ')
            fecha, hora = fecha_hora.split(' ')

            mensaje = Mensaje(lugar, fecha, hora, usuario, red_social, texto)
            mensajes.append(mensaje)

        # Aquí puedes retornar o procesar las listas de empresas y mensajes como necesites
        return empresas, mensajes  # O lo que necesites hacer con ellos

    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
        raise  # Lanzar la excepción para que sea capturada en la función cargar
    except Exception as e:
        print(f"Error en leerarchivo: {e}")
        raise  # Lanzar la excepción para que sea capturada en la función cargar