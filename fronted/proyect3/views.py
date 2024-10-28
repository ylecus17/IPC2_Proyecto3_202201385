from django.shortcuts import render
import requests

def home(request):
    return render(request, 'home.html')

def cargar_archivo(request):
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
                # Leer el contenido del archivo XML devuelto por Flask como texto
                contenido_archivo = response.text
                mensaje = 'Archivo enviado y recibido correctamente'
            else:
                mensaje = 'Error al enviar el archivo'
                contenido_archivo = '  '
        except Exception as e:
            mensaje = f'Error al conectar con el backend: {e}'
            contenido_archivo = ''

        return render(request, 'cargar.html', {
            'mensaje': mensaje,
            'contenido_archivo': contenido_archivo
        })

    return render(request, 'cargar.html')

def peticiones(request):
    return render(request, 'peticiones.html')

def ayuda(request):
    return render(request, 'ayuda.html')
