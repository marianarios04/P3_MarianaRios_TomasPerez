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
            if not os.path.exists(carpeta):
                print("La ruta proporcionada no existe.")
                continue

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

        elif opcion == 'd':
            clave = input("Clave del DICOM para transformar: ")
            if clave in dic_archivos:
                try:
                    img = dic_archivos[clave].dicom_objs[0].pixel_array
                    opciones = [(20, 30), (50, 10), (0, 100), (-30, -10)]
                    for i, (dx, dy) in enumerate(opciones):
                        print(f"{i+1}. Trasladar {dx}px horizontal y {dy}px vertical")
                    try:
                        eleccion = int(input("Seleccione opción de traslación: "))
                        if eleccion < 1 or eleccion > len(opciones):
                            raise ValueError("Opción fuera de rango.")
                        dx, dy = opciones[eleccion - 1]
                    except ValueError as e:
                        print(f"Entrada inválida: {e}")
                        continue
                    M = np.float32([[1, 0, dx], [0, 1, dy]])
                    trasladada = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
                    fig, (ax1, ax2) = plt.subplots(1, 2)
                    ax1.imshow(img, cmap='gray')
                    ax1.set_title("Original")
                    ax2.imshow(trasladada, cmap='gray')
                    ax2.set_title("Trasladada")
                    plt.show()
                    cv2.imwrite("dicom_trasladado.png", trasladada)
                    print("Imagen trasladada guardada como 'dicom_trasladado.png'.")
                except Exception as e:
                    print(f"Error en transformación geométrica: {e}")
            else:
                print("Clave no encontrada.")

        elif opcion == 'e':
            clave = input("Clave de imagen JPG/PNG: ")
            if clave in dic_archivos:
                try:
                    img_obj = dic_archivos[clave]
                    print("Métodos: binario, binario_invertido, truncado, tozero, tozero_invertido")
                    metodo = input("Elija método de binarización: ")
                    try:
                        kernel = int(input("Tamaño del kernel: "))
                        if kernel <= 0:
                            raise ValueError("El tamaño del kernel debe ser un entero positivo.")
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                    forma = input("Forma a dibujar (circulo/cuadrado): ")
                    if forma.lower() not in ['circulo', 'cuadrado']:
                        print("Forma no válida. Debe ser 'circulo' o 'cuadrado'.")
                        continue

                    img_obj.binarizar(metodo)
                    img_obj.morfologia(kernel)
                    img_obj.dibujar_forma_y_texto(forma, kernel)

                    nombre_archivo = f"{clave}_procesada.png"
                    cv2.imwrite(nombre_archivo, img_obj.img_final)
                    print(f"Imagen procesada guardada como {nombre_archivo}")
                except Exception as e:
                    print(f"Error al procesar

        elif opcion == 'f':
            print("Saliendo del sistema.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

menu()