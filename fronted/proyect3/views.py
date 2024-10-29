from django.shortcuts import render
import requests

def home(request):
    return render(request, 'home.html')

def cargar_archivo(request):
    mensaje = ''
    contenido_archivo = ''
    contenido_resumen = ''

    if request.method == 'POST':
        # Obtener el archivo del formulario
        archivo = request.FILES['archivo']
        print(f"Archivo recibido en Django: {archivo}")  # Depuración

        try:
            # Enviar el archivo al backend Flask
            response = requests.post(
                'http://127.0.0.1:5000/api/cargar',
                files={'archivo': archivo}
            )

            if response.status_code == 200:
                data = response.json()
                contenido_archivo = data.get('contenido_archivo', '')  # Contenido del archivo procesado
                mensaje = data.get('mensaje', '')

                # Obtener el contenido del archivo resumen
                resumen_response = requests.get('http://127.0.0.1:5000/api/resumen')  # Cambia esta URL según tu API
                if resumen_response.status_code == 200:
                    contenido_resumen = resumen_response.text
                else:
                    contenido_resumen = 'No se pudo obtener el archivo resumen.'

            else:
                mensaje = 'Error al enviar el archivo'

        except Exception as e:
            mensaje = f'Error al conectar con el backend: {e}'

    return render(request, 'cargar.html', {
        'mensaje': mensaje,
        'contenido_archivo': contenido_archivo,  # Contenido del archivo original
        'contenido_resumen': contenido_resumen,  # Contenido del archivo resumen
    })
def peticiones(request):
    return render(request, 'peticiones.html')

def ver_datos(request):
    mensaje = ''
    contenido_resumen = ''

    try:
        response = requests.get('http://127.0.0.1:5000/api/ver_datos')
        if response.status_code == 200:
            contenido_resumen = response.content.decode('utf-8')
        else:
            mensaje = 'Error al obtener los datos'
    except Exception as e:
        mensaje = f'Error al conectar con el backend: {e}'

    return render(request, 'ver_datos.html', {'mensaje': mensaje, 'contenido_resumen': contenido_resumen})

def filtrar_fecha(request):
    mensaje = ''
    contenido_resumen = ''

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        empresa = request.POST.get('empresa')

        try:
            response = requests.post(
                'http://127.0.0.1:5000/api/filtrar_resumen',
                data={'fecha': fecha, 'empresa': empresa}
            )
            if response.status_code == 200:
                response_xml = requests.get('http://127.0.0.1:5000/api/fecha_filter')
                if response_xml.status_code == 200:
                    contenido_resumen = response_xml.content.decode('utf-8')
                else:
                    mensaje = 'Error al obtener el archivo filtrado'
            else:
                mensaje = 'Error al filtrar los resultados'
        except Exception as e:
            mensaje = f'Error al conectar con el backend: {e}'

    return render(request, 'filtrar_fecha.html', {'mensaje': mensaje, 'contenido_resumen': contenido_resumen})

def filtrar_rango(request):
    mensaje = ''
    contenido_resumen = ''

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        empresa = request.POST.get('empresa')

        try:
            # Enviar la solicitud POST al backend de Flask
            response = requests.post(
                'http://127.0.0.1:5000/api/filtrar_rango',
                data={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'empresa': empresa}
            )

            if response.status_code == 200:
                # Solicitar el archivo XML filtrado
                response_xml = requests.get('http://127.0.0.1:5000/api/rango_filter')
                
                if response_xml.status_code == 200:
                    contenido_resumen = response_xml.content.decode('utf-8')
                else:
                    mensaje = 'Error al obtener el archivo filtrado'
            else:
                mensaje = 'Error al filtrar los resultados'
        except Exception as e:
            mensaje = f'Error al conectar con el backend: {e}'

    return render(request, 'filtrar_rango.html', {'mensaje': mensaje, 'contenido_resumen': contenido_resumen})
def ver_mensajes(request):
    mensaje = ''
    contenido_resumen = ''

    try:
        response = requests.get('http://127.0.0.1:5000/api/ver_mensajes')
        if response.status_code == 200:
            contenido_resumen = response.content.decode('utf-8')
        else:
            mensaje = 'Error al obtener los mensajes'
    except Exception as e:
        mensaje = f'Error al conectar con el backend: {e}'

    return render(request, 'ver_mensajes.html', {'mensaje': mensaje, 'contenido_resumen': contenido_resumen})
def ayuda(request):
    return render(request, 'ayuda.html')
