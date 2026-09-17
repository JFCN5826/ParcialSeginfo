import subprocess
import itertools
import sys

archivos_gpg = ["A.pdf.gpg", "B.pdf.gpg", "C.pdf.gpg", "D.pdf.gpg"]

ciudades_base = [
    "canberra", "sydney", "santiago", "chile", "barcelona", "madrid", 
    "new york", "newyork", "paris", "london", "dubai", "medellin", 
    "mexico city", "mexico", "rome", "tokyo", "seoul", "singapore", 
    "prague", "buenos aires", "toronto", "vienna", "lisbon"
]

# Generar variaciones únicas
variaciones = set()
for c in ciudades_base:
    variaciones.add(c.lower())
    variaciones.add(c.title())
    variaciones.add(c.upper())
    variaciones.add(c.replace(" ", ""))
    variaciones.add(c.title().replace(" ", ""))

ciudades = list(variaciones)

passphrases = []
for c1, c2 in itertools.product(ciudades, repeat=2):
    passphrases.extend([f"{c1}{c2}", f"{c1} {c2}", f"{c1}-{c2}", f"{c1}_{c2}"])

passphrases = list(set(passphrases))
total_intentos = len(passphrases)

print(f"Iniciando ataque optimizado con {total_intentos} contraseñas...")

archivo_prueba = archivos_gpg[0]
archivo_salida = archivo_prueba.replace(".gpg", "")

for i, pwd in enumerate(passphrases, 1):
    if i % 100 == 0 or i == total_intentos:
        porcentaje = (i / total_intentos) * 100
        sys.stdout.write(f"\rProbando: {i}/{total_intentos} ({porcentaje:.2f}%)")
        sys.stdout.flush()

    comando_prueba = [
        "gpg", "--batch", "--yes", "--passphrase", pwd,
        "--output", archivo_salida, "--decrypt", archivo_prueba
    ]
    
    try:
        # Añadimos un timeout de 3 segundos por seguridad para que nunca se quede colgado
        resultado = subprocess.run(comando_prueba, capture_output=True, timeout=3)
        
        if resultado.returncode == 0:
            print("\n\n" + "="*50)
            print(f"¡ÉXITO! La contraseña correcta es: '{pwd}'")
            print("Descifrando el resto de los archivos automáticamente...")
            print("="*50)
            
            for archivo in archivos_gpg[1:]:
                salida = archivo.replace(".gpg", "")
                comando_descifrar = [
                    "gpg", "--batch", "--yes", "--passphrase", pwd,
                    "--output", salida, "--decrypt", archivo
                ]
                subprocess.run(comando_descifrar, capture_output=True)
                print(f"[OK] -> {archivo} descifrado como {salida}")
            
            print("\n¡Trabajo terminado! Revisa tu carpeta.")
            sys.exit(0)
            
    except subprocess.TimeoutExpired:
        # Si un intento tarda más de 3 segundos, lo ignoramos y seguimos
        continue

print("\n\nBúsqueda finalizada. No se encontró la contraseña.")
