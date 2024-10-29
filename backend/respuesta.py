import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
import globales
from datetime import datetime
global empresasr
empresasr = []
mensajesr = []
positivosr = []
negativosr = []

def clasificar_mensaje(mensaje, positivos, negativos):
    contenido = mensaje.contenido.lower()
    positivos_encontrados = sum(1 for p in positivos if p in contenido)
    negativos_encontrados = sum(1 for n in negativos if n in contenido)

    if positivos_encontrados > negativos_encontrados:
        return "positivo"
    elif negativos_encontrados > positivos_encontrados:
        return "negativo"
    else:
        return "neutro"


def generar_xml_resumen():
    
    empresas = globales.empresas
    mensajes = globales.mensajes
    positivos = globales.positivos
    negativos = globales.negativos
    
    
    agrupado_por_fecha = defaultdict(lambda: {"mensajes": [], "positivos": 0, "negativos": 0, "neutros": 0})
    agrupado_por_empresa = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

    # Agrupar mensajes por fecha
    for mensaje in mensajes:
        agrupado_por_fecha[mensaje.fecha]["mensajes"].append(mensaje)

    root = ET.Element("lista_respuestas")

    for fecha, data in agrupado_por_fecha.items():
        mensajes_fecha = data["mensajes"]
        total_mensajes = len(mensajes_fecha)

        # Contadores totales por fecha
        contador_positivos_total = 0
        contador_negativos_total = 0
        contador_neutros_total = 0

        # Lista temporal para mensajes de empresas
        mensajes_empresa = defaultdict(list)

        for mensaje in mensajes_fecha:
            clasificacion = clasificar_mensaje(mensaje, positivos, negativos)

            if clasificacion == "positivo":
                contador_positivos_total += 1
            elif clasificacion == "negativo":
                contador_negativos_total += 1
            else:
                contador_neutros_total += 1

            # Buscar coincidencias con empresas
            for empresa in empresas:
                if empresa.nombre.lower() in mensaje.contenido.lower():
                    mensajes_empresa[empresa.nombre].append(mensaje)
                    break  # Salir si se encuentra la empresa

        # Agregar información de la fecha al XML
        fecha_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(fecha_elem, "fecha").text = fecha
        mensajes_elem = ET.SubElement(fecha_elem, "mensajes")
        ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
        ET.SubElement(mensajes_elem, "positivos").text = str(contador_positivos_total)
        ET.SubElement(mensajes_elem, "negativos").text = str(contador_negativos_total)
        ET.SubElement(mensajes_elem, "neutros").text = str(contador_neutros_total)

        # Agregar análisis por empresa
        analisis_elem = ET.SubElement(fecha_elem, "analisis")

        for nombre_empresa, mensajes in mensajes_empresa.items():
            contador_positivos_empresa = 0
            contador_negativos_empresa = 0
            contador_neutros_empresa = 0
            mensajes_servicio = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

            for mensaje in mensajes:
                clasificacion = clasificar_mensaje(mensaje, positivos, negativos)
                if clasificacion == "positivo":
                    contador_positivos_empresa += 1
                elif clasificacion == "negativo":
                    contador_negativos_empresa += 1
                else:
                    contador_neutros_empresa += 1

                # Clasificar por servicios basados en nombre y alias
                for servicio in [s for e in empresas if e.nombre == nombre_empresa for s in e.servicios]:
                    # Comparar el nombre del servicio
                    if servicio.nombre.lower() in mensaje.contenido.lower():
                        mensajes_servicio[servicio.nombre]["total"] += 1
                        if clasificacion == "positivo":
                            mensajes_servicio[servicio.nombre]["positivos"] += 1
                        elif clasificacion == "negativo":
                            mensajes_servicio[servicio.nombre]["negativos"] += 1
                        else:
                            mensajes_servicio[servicio.nombre]["neutros"] += 1
                        break  # Salir si se encuentra el nombre del servicio

                    # Comparar los alias del servicio
                    for alias in servicio.alias:
                        if alias.lower() in mensaje.contenido.lower():
                            mensajes_servicio[servicio.nombre]["total"] += 1
                            if clasificacion == "positivo":
                                mensajes_servicio[servicio.nombre]["positivos"] += 1
                            elif clasificacion == "negativo":
                                mensajes_servicio[servicio.nombre]["negativos"] += 1
                            else:
                                mensajes_servicio[servicio.nombre]["neutros"] += 1
                            break  # Salir si se encuentra un alias

            # Crear elemento para la empresa en el XML
            empresa_elem = ET.SubElement(analisis_elem, "empresa", nombre=nombre_empresa)
            mensajes_empresa_elem = ET.SubElement(empresa_elem, "mensajes")
            ET.SubElement(mensajes_empresa_elem, "total").text = str(len(mensajes))
            ET.SubElement(mensajes_empresa_elem, "positivos").text = str(contador_positivos_empresa)
            ET.SubElement(mensajes_empresa_elem, "negativos").text = str(contador_negativos_empresa)
            ET.SubElement(mensajes_empresa_elem, "neutros").text = str(contador_neutros_empresa)

            # Agregar análisis por servicios
            servicios_elem = ET.SubElement(empresa_elem, "servicios")
            for nombre_servicio, data in mensajes_servicio.items():
                servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=nombre_servicio)
                mensajes_servicio_elem = ET.SubElement(servicio_elem, "mensajes")
                ET.SubElement(mensajes_servicio_elem, "total").text = str(data["total"])
                ET.SubElement(mensajes_servicio_elem, "positivos").text = str(data["positivos"])
                ET.SubElement(mensajes_servicio_elem, "negativos").text = str(data["negativos"])
                ET.SubElement(mensajes_servicio_elem, "neutros").text = str(data["neutros"])

    return ET.ElementTree(root)


def guardar_xml(archivo_xml, nombre_archivo):
    rough_string = ET.tostring(archivo_xml.getroot(), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    return nombre_archivo  

def convertir_fecha(fecha_str):
    try:
        # Intentar convertir desde el formato DD/MM/YYYY
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        # Si falla, intentar convertir desde el formato YYYY-MM-DD
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()

def filtrar_por_fecha(fechaF):
    fecha_convertida = convertir_fecha(fechaF)  # Convertir la fecha de entrada
    print(globales.empresas)  # Asegúrate de que globales.empresas esté correctamente definido

    # Crear un defaultdict para agrupar los mensajes
    agrupado_por_empresa = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})
    mensajes_fecha = []  # Lista para almacenar mensajes de la fecha específica

    # Filtrar mensajes por la fecha especificada
    for mensaje in globales.mensajes:
        if convertir_fecha(mensaje.fecha) == fecha_convertida:  # Comparar las fechas convertidas
            mensajes_fecha.append(mensaje)

    root = ET.Element("lista_respuestas")
    total_mensajes = len(mensajes_fecha)
    contador_positivos_total = 0
    contador_negativos_total = 0
    contador_neutros_total = 0
    mensajes_empresa = defaultdict(list)

    # Si no se encontraron mensajes, agregar un mensaje al XML
    if total_mensajes == 0:
        fecha_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(fecha_elem, "fecha").text = fechaF
        ET.SubElement(fecha_elem, "mensaje").text = "No se encontraron coincidencias"
        return ET.ElementTree(root)

    for mensaje in mensajes_fecha:
        clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
        if clasificacion == "positivo":
            contador_positivos_total += 1
        elif clasificacion == "negativo":
            contador_negativos_total += 1
        else:
            contador_neutros_total += 1

        # Buscar coincidencias con empresas
        for empresa in globales.empresas:
            if empresa.nombre.lower() in mensaje.contenido.lower():
                mensajes_empresa[empresa.nombre].append(mensaje)
                break

    # Agregar información de la fecha al XML
    fecha_elem = ET.SubElement(root, "respuesta")
    ET.SubElement(fecha_elem, "fecha").text = fechaF
    mensajes_elem = ET.SubElement(fecha_elem, "mensajes")
    ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
    ET.SubElement(mensajes_elem, "positivos").text = str(contador_positivos_total)
    ET.SubElement(mensajes_elem, "negativos").text = str(contador_negativos_total)
    ET.SubElement(mensajes_elem, "neutros").text = str(contador_neutros_total)

    # Agregar análisis por empresa
    analisis_elem = ET.SubElement(fecha_elem, "analisis")

    for nombre_empresa, mensajes in mensajes_empresa.items():
        contador_positivos_empresa = 0
        contador_negativos_empresa = 0
        contador_neutros_empresa = 0
        mensajes_servicio = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

        for mensaje in mensajes:
            clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
            if clasificacion == "positivo":
                contador_positivos_empresa += 1
            elif clasificacion == "negativo":
                contador_negativos_empresa += 1
            else:
                contador_neutros_empresa += 1

            # Clasificar por servicios
            for servicio in [s for e in globales.empresas if e.nombre == nombre_empresa for s in e.servicios]:
                if servicio.nombre.lower() in mensaje.contenido.lower() or any(alias.lower() in mensaje.contenido.lower() for alias in servicio.alias):
                    mensajes_servicio[servicio.nombre]["total"] += 1
                    if clasificacion == "positivo":
                        mensajes_servicio[servicio.nombre]["positivos"] += 1
                    elif clasificacion == "negativo":
                        mensajes_servicio[servicio.nombre]["negativos"] += 1
                    else:
                        mensajes_servicio[servicio.nombre]["neutros"] += 1
                    break

        # Crear elemento para la empresa en el XML
        empresa_elem = ET.SubElement(analisis_elem, "empresa", nombre=nombre_empresa)
        mensajes_empresa_elem = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(mensajes_empresa_elem, "total").text = str(len(mensajes))
        ET.SubElement(mensajes_empresa_elem, "positivos").text = str(contador_positivos_empresa)
        ET.SubElement(mensajes_empresa_elem, "negativos").text = str(contador_negativos_empresa)
        ET.SubElement(mensajes_empresa_elem, "neutros").text = str(contador_neutros_empresa)

        # Agregar análisis por servicios
        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for nombre_servicio, data in mensajes_servicio.items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=nombre_servicio)
            mensajes_servicio_elem = ET.SubElement(servicio_elem, "mensajes")
            ET.SubElement(mensajes_servicio_elem, "total").text = str(data["total"])
            ET.SubElement(mensajes_servicio_elem, "positivos").text = str(data["positivos"])
            ET.SubElement(mensajes_servicio_elem, "negativos").text = str(data["negativos"])
            ET.SubElement(mensajes_servicio_elem, "neutros").text = str(data["neutros"])

    return ET.ElementTree(root)

def filtrar_por_fecha_y_empresa(fechaF, empresaN):
    fecha_convertida = convertir_fecha(fechaF)  # Convertir la fecha de entrada
    print(globales.empresas)  # Asegúrate de que globales.empresas esté correctamente definido

    # Crear un defaultdict para agrupar los mensajes
    agrupado_por_empresa = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})
    mensajes_fecha = []  # Lista para almacenar mensajes de la fecha específica

    # Filtrar mensajes por la fecha especificada
    for mensaje in globales.mensajes:
        if convertir_fecha(mensaje.fecha) == fecha_convertida:  # Comparar las fechas convertidas
            mensajes_fecha.append(mensaje)

    root = ET.Element("lista_respuestas")
    total_mensajes = len(mensajes_fecha)
    contador_positivos_total = 0
    contador_negativos_total = 0
    contador_neutros_total = 0
    mensajes_empresa = defaultdict(list)

    # Si no se encontraron mensajes para la fecha, agregar un mensaje al XML
    if total_mensajes == 0:
        fecha_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(fecha_elem, "fecha").text = fechaF
        ET.SubElement(fecha_elem, "mensaje").text = f"No se encontraron coincidencias para la fecha especificada."
        return ET.ElementTree(root)

    # Buscar coincidencias con empresas
    for mensaje in mensajes_fecha:
        clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
        if clasificacion == "positivo":
            contador_positivos_total += 1
        elif clasificacion == "negativo":
            contador_negativos_total += 1
        else:
            contador_neutros_total += 1

        # Verificar si hay coincidencias con la empresa especificada
        if empresaN.lower() in mensaje.contenido.lower():
            mensajes_empresa[empresaN].append(mensaje)

    # Si no se encontraron mensajes para la empresa, agregar un mensaje al XML
    if not mensajes_empresa:
        fecha_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(fecha_elem, "fecha").text = fechaF
        ET.SubElement(fecha_elem, "mensaje").text = f"No se encontraron coincidencias para la empresa '{empresaN}' en la fecha especificada."
        return ET.ElementTree(root)

    # Agregar información de la fecha al XML
    fecha_elem = ET.SubElement(root, "respuesta")
    ET.SubElement(fecha_elem, "fecha").text = fechaF
    mensajes_elem = ET.SubElement(fecha_elem, "mensajes")
    ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
    ET.SubElement(mensajes_elem, "positivos").text = str(contador_positivos_total)
    ET.SubElement(mensajes_elem, "negativos").text = str(contador_negativos_total)
    ET.SubElement(mensajes_elem, "neutros").text = str(contador_neutros_total)

    # Agregar análisis por empresa
    analisis_elem = ET.SubElement(fecha_elem, "analisis")

    for nombre_empresa, mensajes in mensajes_empresa.items():
        contador_positivos_empresa = 0
        contador_negativos_empresa = 0
        contador_neutros_empresa = 0
        mensajes_servicio = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

        for mensaje in mensajes:
            clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
            if clasificacion == "positivo":
                contador_positivos_empresa += 1
            elif clasificacion == "negativo":
                contador_negativos_empresa += 1
            else:
                contador_neutros_empresa += 1

            # Clasificar por servicios
            for servicio in [s for e in globales.empresas if e.nombre == nombre_empresa for s in e.servicios]:
                if servicio.nombre.lower() in mensaje.contenido.lower() or any(alias.lower() in mensaje.contenido.lower() for alias in servicio.alias):
                    mensajes_servicio[servicio.nombre]["total"] += 1
                    if clasificacion == "positivo":
                        mensajes_servicio[servicio.nombre]["positivos"] += 1
                    elif clasificacion == "negativo":
                        mensajes_servicio[servicio.nombre]["negativos"] += 1
                    else:
                        mensajes_servicio[servicio.nombre]["neutros"] += 1
                    break

        # Crear elemento para la empresa en el XML
        empresa_elem = ET.SubElement(analisis_elem, "empresa", nombre=nombre_empresa)
        mensajes_empresa_elem = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(mensajes_empresa_elem, "total").text = str(len(mensajes))
        ET.SubElement(mensajes_empresa_elem, "positivos").text = str(contador_positivos_empresa)
        ET.SubElement(mensajes_empresa_elem, "negativos").text = str(contador_negativos_empresa)
        ET.SubElement(mensajes_empresa_elem, "neutros").text = str(contador_neutros_empresa)

        # Agregar análisis por servicios
        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for nombre_servicio, data in mensajes_servicio.items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=nombre_servicio)
            mensajes_servicio_elem = ET.SubElement(servicio_elem, "mensajes")
            ET.SubElement(mensajes_servicio_elem, "total").text = str(data["total"])
            ET.SubElement(mensajes_servicio_elem, "positivos").text = str(data["positivos"])
            ET.SubElement(mensajes_servicio_elem, "negativos").text = str(data["negativos"])
            ET.SubElement(mensajes_servicio_elem, "neutros").text = str(data["neutros"])

    return ET.ElementTree(root)


def filtrar_por_rango_fechas(fecha_inicio, fecha_fin):
    fecha_inicio_convertida = convertir_fecha(fecha_inicio)  # Convertir la fecha de inicio
    fecha_fin_convertida = convertir_fecha(fecha_fin)  # Convertir la fecha de fin

    # Crear un defaultdict para agrupar los mensajes
    agrupado_por_empresa = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})
    mensajes_en_rango = []  # Lista para almacenar mensajes dentro del rango específico

    # Filtrar mensajes por el rango de fechas especificado
    for mensaje in globales.mensajes:
        fecha_mensaje_convertida = convertir_fecha(mensaje.fecha)
        if fecha_inicio_convertida <= fecha_mensaje_convertida <= fecha_fin_convertida:
            mensajes_en_rango.append(mensaje)

    root = ET.Element("lista_respuestas")
    total_mensajes = len(mensajes_en_rango)
    contador_positivos_total = 0
    contador_negativos_total = 0
    contador_neutros_total = 0
    mensajes_empresa = defaultdict(list)

    # Si no se encontraron mensajes, agregar un mensaje al XML
    if total_mensajes == 0:
        respuesta_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(respuesta_elem, "rango").text = f"{fecha_inicio} a {fecha_fin}"
        ET.SubElement(respuesta_elem, "mensaje").text = "No se encontraron coincidencias en el rango de fechas"
        return ET.ElementTree(root)

    # Agregar las fechas de los mensajes encontrados
    fechas_mensajes = set()
    for mensaje in mensajes_en_rango:
        fechas_mensajes.add(mensaje.fecha)

    for mensaje in mensajes_en_rango:
        clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
        if clasificacion == "positivo":
            contador_positivos_total += 1
        elif clasificacion == "negativo":
            contador_negativos_total += 1
        else:
            contador_neutros_total += 1

        # Buscar coincidencias con empresas
        for empresa in globales.empresas:
            if empresa.nombre.lower() in mensaje.contenido.lower():
                mensajes_empresa[empresa.nombre].append(mensaje)
                break

    # Agregar información del rango de fechas al XML
    respuesta_elem = ET.SubElement(root, "respuesta")
    ET.SubElement(respuesta_elem, "rango").text = f"{fecha_inicio} a {fecha_fin}"
    mensajes_elem = ET.SubElement(respuesta_elem, "mensajes")
    ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
    ET.SubElement(mensajes_elem, "positivos").text = str(contador_positivos_total)
    ET.SubElement(mensajes_elem, "negativos").text = str(contador_negativos_total)
    ET.SubElement(mensajes_elem, "neutros").text = str(contador_neutros_total)

    # Agregar análisis por empresa
    analisis_elem = ET.SubElement(respuesta_elem, "analisis")

    for nombre_empresa, mensajes in mensajes_empresa.items():
        contador_positivos_empresa = 0
        contador_negativos_empresa = 0
        contador_neutros_empresa = 0
        mensajes_servicio = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

        for mensaje in mensajes:
            clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
            if clasificacion == "positivo":
                contador_positivos_empresa += 1
            elif clasificacion == "negativo":
                contador_negativos_empresa += 1
            else:
                contador_neutros_empresa += 1

            # Clasificar por servicios
            for servicio in [s for e in globales.empresas if e.nombre == nombre_empresa for s in e.servicios]:
                if servicio.nombre.lower() in mensaje.contenido.lower() or any(alias.lower() in mensaje.contenido.lower() for alias in servicio.alias):
                    mensajes_servicio[servicio.nombre]["total"] += 1
                    if clasificacion == "positivo":
                        mensajes_servicio[servicio.nombre]["positivos"] += 1
                    elif clasificacion == "negativo":
                        mensajes_servicio[servicio.nombre]["negativos"] += 1
                    else:
                        mensajes_servicio[servicio.nombre]["neutros"] += 1
                    break

        # Crear elemento para la empresa en el XML
        empresa_elem = ET.SubElement(analisis_elem, "empresa", nombre=nombre_empresa)
        mensajes_empresa_elem = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(mensajes_empresa_elem, "total").text = str(len(mensajes))
        ET.SubElement(mensajes_empresa_elem, "positivos").text = str(contador_positivos_empresa)
        ET.SubElement(mensajes_empresa_elem, "negativos").text = str(contador_negativos_empresa)
        ET.SubElement(mensajes_empresa_elem, "neutros").text = str(contador_neutros_empresa)

        # Agregar análisis por servicios
        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for nombre_servicio, data in mensajes_servicio.items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=nombre_servicio)
            mensajes_servicio_elem = ET.SubElement(servicio_elem, "mensajes")
            ET.SubElement(mensajes_servicio_elem, "total").text = str(data["total"])
            ET.SubElement(mensajes_servicio_elem, "positivos").text = str(data["positivos"])
            ET.SubElement(mensajes_servicio_elem, "negativos").text = str(data["negativos"])
            ET.SubElement(mensajes_servicio_elem, "neutros").text = str(data["neutros"])

    return ET.ElementTree(root)
def filtrar_por_rango_fechas_y_empresa(fecha_inicio, fecha_fin, empresa_nombre):
    fecha_inicio_convertida = convertir_fecha(fecha_inicio)
    fecha_fin_convertida = convertir_fecha(fecha_fin)
    
    # Crear un defaultdict para agrupar los mensajes
    agrupado_por_empresa = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})
    mensajes_en_rango = []  # Lista para almacenar mensajes dentro del rango

    # Filtrar mensajes por el rango de fechas especificado
    for mensaje in globales.mensajes:
        fecha_mensaje_convertida = convertir_fecha(mensaje.fecha)
        if fecha_inicio_convertida <= fecha_mensaje_convertida <= fecha_fin_convertida:  # Comparar fechas
            mensajes_en_rango.append(mensaje)

    root = ET.Element("lista_respuestas")
    total_mensajes = len(mensajes_en_rango)
    contador_positivos_total = 0
    contador_negativos_total = 0
    contador_neutros_total = 0
    mensajes_empresa = defaultdict(list)

    # Si no se encontraron mensajes, agregar un mensaje al XML
    if total_mensajes == 0:
        fecha_elem = ET.SubElement(root, "respuesta")
        ET.SubElement(fecha_elem, "fecha").text = f"Del {fecha_inicio} al {fecha_fin}"
        ET.SubElement(fecha_elem, "mensaje").text = "No se encontraron coincidencias"
        return ET.ElementTree(root)

    for mensaje in mensajes_en_rango:
        clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
        if clasificacion == "positivo":
            contador_positivos_total += 1
        elif clasificacion == "negativo":
            contador_negativos_total += 1
        else:
            contador_neutros_total += 1

        # Filtrar por empresa si se especifica
        if empresa_nombre and empresa_nombre.lower() in mensaje.contenido.lower():
            mensajes_empresa[empresa_nombre].append(mensaje)

    # Agregar información del rango al XML
    fecha_elem = ET.SubElement(root, "respuesta")
    ET.SubElement(fecha_elem, "rango_fechas").text = f"Del {fecha_inicio} al {fecha_fin}"
    mensajes_elem = ET.SubElement(fecha_elem, "mensajes")
    ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
    ET.SubElement(mensajes_elem, "positivos").text = str(contador_positivos_total)
    ET.SubElement(mensajes_elem, "negativos").text = str(contador_negativos_total)
    ET.SubElement(mensajes_elem, "neutros").text = str(contador_neutros_total)

    # Agregar análisis por empresa
    analisis_elem = ET.SubElement(fecha_elem, "analisis")

    for nombre_empresa, mensajes in mensajes_empresa.items():
        contador_positivos_empresa = 0
        contador_negativos_empresa = 0
        contador_neutros_empresa = 0
        mensajes_servicio = defaultdict(lambda: {"total": 0, "positivos": 0, "negativos": 0, "neutros": 0})

        for mensaje in mensajes:
            clasificacion = clasificar_mensaje(mensaje, globales.positivos, globales.negativos)
            if clasificacion == "positivo":
                contador_positivos_empresa += 1
            elif clasificacion == "negativo":
                contador_negativos_empresa += 1
            else:
                contador_neutros_empresa += 1

            # Clasificar por servicios
            for servicio in [s for e in globales.empresas if e.nombre.lower() == nombre_empresa.lower() for s in e.servicios]:
                if servicio.nombre.lower() in mensaje.contenido.lower() or any(alias.lower() in mensaje.contenido.lower() for alias in servicio.alias):
                    mensajes_servicio[servicio.nombre]["total"] += 1
                    if clasificacion == "positivo":
                        mensajes_servicio[servicio.nombre]["positivos"] += 1
                    elif clasificacion == "negativo":
                        mensajes_servicio[servicio.nombre]["negativos"] += 1
                    else:
                        mensajes_servicio[servicio.nombre]["neutros"] += 1
                    break

        # Crear elemento para la empresa en el XML
        empresa_elem = ET.SubElement(analisis_elem, "empresa", nombre=nombre_empresa)
        mensajes_empresa_elem = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(mensajes_empresa_elem, "total").text = str(len(mensajes))
        ET.SubElement(mensajes_empresa_elem, "positivos").text = str(contador_positivos_empresa)
        ET.SubElement(mensajes_empresa_elem, "negativos").text = str(contador_negativos_empresa)
        ET.SubElement(mensajes_empresa_elem, "neutros").text = str(contador_neutros_empresa)

        # Agregar análisis por servicios
        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for nombre_servicio, data in mensajes_servicio.items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=nombre_servicio)
            mensajes_servicio_elem = ET.SubElement(servicio_elem, "mensajes")
            ET.SubElement(mensajes_servicio_elem, "total").text = str(data["total"])
            ET.SubElement(mensajes_servicio_elem, "positivos").text = str(data["positivos"])
            ET.SubElement(mensajes_servicio_elem, "negativos").text = str(data["negativos"])
            ET.SubElement(mensajes_servicio_elem, "neutros").text = str(data["neutros"])

    return ET.ElementTree(root)

def procesar_mensaje(xml_input):
    try:
        # Dividir el mensaje en líneas
        lineas = xml_input.strip().split('\n')

        # Inicializar el diccionario para almacenar la información extraída
        informacion = {}

        # Extraer información del mensaje
        lugar_fecha_str = lineas[0].split(': ')[1].strip()  # "Lugar y fecha: Guatemala,"
        lugar, datetime_str = lugar_fecha_str.split(', ')  # "Guatemala" y "01/04/2022 15:20"
        fecha, hora = datetime_str.split(' ')  # "01/04/2022" y "15:20"

        informacion['lugar'] = lugar
        informacion['fecha'] = fecha
        informacion['hora'] = hora
        informacion['usuario'] = lineas[1].split(': ')[1].strip()  # "Usuario: map0002@usac.edu"
        informacion['red_social'] = lineas[2].split(': ')[1].strip()  # "Red social: Facebook"
        informacion['texto'] = lineas[3].strip()  # Texto del mensaje

        return informacion

    except Exception as e:
        print(f"Error al extraer información: {e}")
        return None  # Retornar None si hay un error
    
def generar_txt():
    contenido = "Datos Generados:\n\n"
    
    # Guardar palabras positivas y negativas
    contenido += "Palabras Positivas:\n" + "\n".join(positivos) + "\n\n"
    contenido += "Palabras Negativas:\n" + "\n".join(negativos) + "\n\n"
    
    # Guardar empresas y sus servicios
    contenido += "Empresas y sus servicios:\n"
    for empresa in empresas:
        contenido += f"Empresa: {empresa.nombre}\n"
        for servicio in empresa.servicios:
            contenido += f"  Servicio: {servicio.nombre}\n"
            contenido += f"    Aliases: {servicio.alias}\n"

    # Guardar mensajes procesados
    contenido += "\nMensajes Procesados:\n"
    for mensaje in mensajes:
        contenido += f"Lugar: {mensaje.lugar}\n"
        contenido += f"Fecha: {mensaje.fecha}\n"
        contenido += f"Hora: {mensaje.hora}\n"
        contenido += f"Usuario: {mensaje.usuario}\n"
        contenido += f"Red social: {mensaje.red_social}\n"
        contenido += f"Mensaje: {mensaje.contenido}\n\n"

    # Guardar el contenido en un archivo
    with open('datos.txt', 'w') as file:
        file.write(contenido)
