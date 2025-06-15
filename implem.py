import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from clase import Paciente, ImagenDICOM, ImagenSimple

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

        opcion = input("Elija una opción: ").lower()

        if opcion == 'a':
            carpeta = input("Ruta carpeta DICOM: ")
            clave = input("Nombre clave para guardar: ")
            try:
                dicom = ImagenDICOM(carpeta)
                if dicom.volumen.size == 0:
                    print("No se pudo crear el volumen 3D.")
                    continue
                dicom.mostrar_cortes()
                dic_archivos[clave] = dicom
                print(f"Carpeta {clave} procesada y guardada.")
            except Exception as e:
                print(f"Error al procesar carpeta DICOM: {e}")

        elif opcion == 'b':
            clave = input("Clave del DICOM para paciente: ")
            if clave in dic_archivos:
                try:
                    dicom = dic_archivos[clave]
                    nombre, edad, id_pac = dicom.obtener_info_paciente()
                    paciente = Paciente(nombre, edad, id_pac, dicom.volumen)
                    dic_pacientes[id_pac] = paciente
                    print(f"Paciente {nombre} creado con ID {id_pac}.")
                except Exception as e:
                    print(f"Error al ingresar paciente: {e}")
            else:
                print("Clave no encontrada.")

        elif opcion == 'c':
            ruta = input("Ruta de imagen PNG/JPG: ")
            clave = input("Clave para guardar imagen: ")
            try:
                img = ImagenSimple(ruta)
                dic_archivos[clave] = img
                print(f"Imagen {clave} cargada.")
            except Exception as e:
                print(f"Error al cargar imagen: {e}")