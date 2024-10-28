class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def __repr__(self):
        return f"Empresa(nombre={self.nombre}, servicios={self.servicios})"


class Servicio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []

    def agregar_alias(self, alias):
        self.alias.append(alias)

    def __repr__(self):
        return f"Servicio(nombre={self.nombre}, alias={self.alias})"


class Mensaje:
    def __init__(self, lugar, fecha, hora, usuario, red_social, contenido):
        self.lugar = lugar
        self.fecha = fecha
        self.hora = hora
        self.usuario = usuario
        self.red_social = red_social
        self.contenido = contenido

    def __repr__(self):
        return (
            f"Mensaje(lugar={self.lugar}, fecha={self.fecha}, "
            f"hora={self.hora}, usuario={self.usuario}, "
            f"red_social={self.red_social}, contenido={self.contenido})"
        )


class Diccionario:
    def __init__(self):
        self.positivos = []
        self.negativos = []

    def agregar_positivo(self, palabra):
        self.positivos.append(palabra)

    def agregar_negativo(self, palabra):
        self.negativos.append(palabra)

    def __repr__(self):
        return f"Diccionario(positivos={self.positivos}, negativos={self.negativos})"
