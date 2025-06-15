import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

dic_pacientes = {}
dic_archivos = {}

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("a. Procesar carpeta DICOM")
        print("b. Ingresar paciente")
        print("c. Ingresar imagen JPG/PNG")
        print("d. Transformación geométrica (DICOM)")
        print("e. Procesar imagen simple (binarización y morfología)")
        print("f. Salir")
