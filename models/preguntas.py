import json

class Pregunta:
    """Esta clase representa a las preguntas del juego
    """
    def __init__(self, id, pregunta, opciones):
        self.id = id
        self.pregunta = pregunta
        self.opciones = opciones

    @staticmethod
    def cargar_las_preguntas():
        """Carga las preguntas desde el JSON y arma una lista de objetos Pregunta
        """
        with open('C:/Users/julia/OneDrive/Escritorio/this_or_that/preguntas.json', 'r') as archivo:
            datos_pregunta = json.load(archivo)
        preguntas = []
        for datos in datos_pregunta:
            pregunta = Pregunta(datos['id'], datos['pregunta'], datos['opciones'])
            preguntas.append(pregunta)
        return preguntas
    