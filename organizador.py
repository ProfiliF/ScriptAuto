import os
import sys
import shutil

# Diccionario que asocia carpetas con extensiones de archivo
EXTENSIONES = {
    'Imágenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Comprimidos': ['.zip', '.rar', '.tar.gz', '.7z'],
    'Ejecutables': ['.exe', '.msi', '.bat'],
    'Otros': []  # Aseguramos que 'Otros' esté incluido
}

# Diccionario para almacenar los archivos por categoría
archivos_por_categoria = {}

def organizar_archivos(ruta):
    # Verifica si la ruta existe
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe.")
        return

    # Inicializa el diccionario para almacenar los archivos por categoría
    for categoria in EXTENSIONES.keys():
        archivos_por_categoria[categoria] = []

    # Recorre todos los elementos en la ruta
    for elemento in os.listdir(ruta):
        ruta_elemento = os.path.join(ruta, elemento)
        # Si es un archivo, lo mueve
        if os.path.isfile(ruta_elemento):
            mover_archivo(ruta, elemento)

    # Al finalizar, mostrar los resultados y generar los archivos CSV
    print("\nResumen de archivos organizados:")
    for categoria, archivos in archivos_por_categoria.items():
        if archivos:
            print(f"\nCategoría: {categoria}")
            archivos.sort()  # Ordenar alfabéticamente
            for archivo in archivos:
                print(f"- {archivo}")
            # Generar archivo CSV
            nombre_csv = f"{categoria}.csv"
            ruta_csv = os.path.join(ruta, nombre_csv)
            with open(ruta_csv, 'w', encoding='utf-8') as f:
                for archivo in archivos:
                    f.write(f"{archivo}\n")
            print(f"Lista guardada en {nombre_csv}")

def mover_archivo(ruta, archivo):
    # Obtiene la extensión del archivo
    extension = os.path.splitext(archivo)[1].lower()
    movido = False
    # Recorre las categorías y extensiones
    for carpeta, extensiones in EXTENSIONES.items():
        if extension in extensiones:
            ruta_carpeta = os.path.join(ruta, carpeta)
            # Crea la carpeta si no existe
            os.makedirs(ruta_carpeta, exist_ok=True)
            # Mueve el archivo a la carpeta correspondiente
            shutil.move(os.path.join(ruta, archivo), os.path.join(ruta_carpeta, archivo))
            print(f"Movido: {archivo} -> {ruta_carpeta}")
            movido = True
            # Añade el archivo a la lista de la categoría
            archivos_por_categoria[carpeta].append(archivo)
            break
    if not movido:
        # Si no coincide con ninguna extensión, va a 'Otros'
        ruta_carpeta = os.path.join(ruta, 'Otros')
        os.makedirs(ruta_carpeta, exist_ok=True)
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta_carpeta, archivo))
        print(f"Movido: {archivo} -> {ruta_carpeta}")
        # Añade el archivo a la lista de 'Otros'
        archivos_por_categoria['Otros'].append(archivo)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ruta_objetivo = sys.argv[1]
        organizar_archivos(ruta_objetivo)
    else:
        print("Por favor, proporciona la ruta de la carpeta a organizar.")
