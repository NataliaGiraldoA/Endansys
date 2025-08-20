from pathlib import Path

# Ruta a la carpeta donde están los archivos
carpeta = Path("C:/Users/Natalia/Desktop/dataset/validation/Zorrillo_listado")  # Cambia esta ruta según tu necesidad

# Prefijo para los nuevos nombres
nuevo_nombre_base = "imagen_"

# Elegir la extensión de los archivos a renombrar (opcional)
extensiones = {".jpg", ".png", ".jpeg", ".bmp"}

# Enumerar y renombrar los archivos
for i, archivo in enumerate(sorted(carpeta.iterdir()), start=1):
    if archivo.is_file() and archivo.suffix.lower() in extensiones:
        nuevo_nombre = f"{nuevo_nombre_base}{i:03d}{archivo.suffix.lower()}"
        nuevo_path = carpeta / nuevo_nombre
        archivo.rename(nuevo_path)
        print(f"{archivo.name} -> {nuevo_nombre}")
