import os
import pydicom
import numpy as np
import cv2
import matplotlib.pyplot as plt

class Paciente:
    def __init__(self, nombre, edad, id_paciente, imagen_3d):
        self.nombre = nombre
        self.edad = edad
        self.id_paciente = id_paciente
        self.imagen_3d = imagen_3d
class ImagenDICOM:
    def __init__(self, carpeta):
        self.carpeta = carpeta
        self.archivos = self._cargar_archivos()
        self.dicom_objs = self._leer_dicom_objs()
        self.volumen = self._reconstruir_volumen()

