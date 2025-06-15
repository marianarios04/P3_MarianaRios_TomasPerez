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
    def _cargar_archivos(self):
        try:
            archivos = [f for f in os.listdir(self.carpeta) if f.endswith('.dcm')]
            archivos_ordenados = sorted(archivos, key=lambda x: int(os.path.splitext(x)[0]))
            if not archivos_ordenados:
                raise ValueError("No se encontraron archivos DICOM en la carpeta.")
            return archivos_ordenados
        except Exception as e:
            print(f"Error al cargar archivos DICOM: {e}")
            return []
    def _leer_dicom_objs(self):
        dicom_objs = []
        for archivo in self.archivos:
            ruta_completa = os.path.join(self.carpeta, archivo)
            try:
                ds = pydicom.dcmread(ruta_completa)
                # Intentamos acceder al pixel_array
                try:
                    _ = ds.pixel_array
                except:
                    ds.decompress()  # Intenta descomprimir si está comprimido
                dicom_objs.append(ds)
            except Exception as e: 
                print(f"Error al leer el archivo {archivo}: {e}")
        return dicom_objs

    def _reconstruir_volumen(self):
        try:
            slices = [d.pixel_array for d in self.dicom_objs if hasattr(d, 'pixel_array')]
            if not slices:
                raise ValueError("No se pudieron extraer las imágenes de los archivos DICOM.")
            volumen = np.stack(slices, axis=-1)
            return volumen
        except Exception as e:
            print(f"Error al reconstruir volumen 3D: {e}")
            return np.array([])

    def mostrar_cortes(self):
        try:
            if self.volumen.size == 0:
                print("Volumen no disponible para mostrar cortes.")
                return
            vol = self.volumen
            fig, axs = plt.subplots(1, 3, figsize=(12, 4))
            axs[0].imshow(vol[:, :, vol.shape[2] // 2], cmap='gray')
            axs[0].set_title("Transversal")
            axs[1].imshow(vol[:, vol.shape[1] // 2, :], cmap='gray')
            axs[1].set_title("Sagital")
            axs[2].imshow(vol[vol.shape[0] // 2, :, :], cmap='gray')
            axs[2].set_title("Coronal")
            for ax in axs:
                ax.axis('off')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error al mostrar cortes: {e}")




