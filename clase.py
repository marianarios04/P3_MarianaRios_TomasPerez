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
    def obtener_info_paciente(self):
        try:
            ds = self.dicom_objs[0]
            nombre = getattr(ds, "PatientName", "Anonimo")
            edad = getattr(ds, "PatientAge", "000Y")
            id_paciente = getattr(ds, "PatientID", "SinID")
            return str(nombre), edad[:3], id_paciente
        except Exception as e:
            print(f"Error al obtener información del paciente: {e}")
            return "Anonimo", "000", "SinID"

class ImagenSimple:
    def __init__(self, ruta):
        self.ruta = ruta
        try:
            self.img = cv2.imread(ruta)
            if self.img is None:
                raise ValueError("No se pudo cargar la imagen.")
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            self.img = np.zeros((100, 100, 3), dtype=np.uint8)

    def binarizar(self, metodo, umbral=127):
        tipos = {
            'binario': cv2.THRESH_BINARY,
            'binario_invertido': cv2.THRESH_BINARY_INV,
            'truncado': cv2.THRESH_TRUNC,
            'tozero': cv2.THRESH_TOZERO,
            'tozero_invertido': cv2.THRESH_TOZERO_INV
        }
        try:
            if metodo not in tipos:
                raise ValueError("Método de binarización inválido.")
            _, self.img_binarizada = cv2.threshold(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY), umbral, 255, tipos[metodo])
        except Exception as e:
            print(f"Error en binarización: {e}")
            self.img_binarizada = self.img.copy()

    def morfologia(self, tam_kernel):
        try:
            kernel = np.ones((tam_kernel, tam_kernel), np.uint8)
            self.img_morf = cv2.morphologyEx(self.img_binarizada, cv2.MORPH_CLOSE, kernel)
        except Exception as e:
            print(f"Error en transformación morfológica: {e}")
            self.img_morf = self.img_binarizada.copy()

    def dibujar_forma_y_texto(self, forma, tam_kernel):
        try:
            img_out = self.img_morf.copy()
            if forma == 'circulo':
                cv2.circle(img_out, (100, 100), 50, (255, 0, 0), 2)
            elif forma == 'cuadrado':
                cv2.rectangle(img_out, (50, 50), (150, 150), (0, 255, 0), 2)
            else:
                raise ValueError("Forma no válida")
            texto = f"Imagen binarizada - Kernel: {tam_kernel}"
            cv2.putText(img_out, texto, (10, img_out.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            self.img_final = img_out
        except Exception as e:
            print(f"Error al dibujar forma y texto: {e}")
            self.img_final = self.img_morf.copy()
        

