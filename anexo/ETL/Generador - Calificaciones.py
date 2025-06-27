import pandas as pd
import numpy as np
import os
import re
import random
import csv

# === Parte 1: Generar el archivo CSV original ===
materias_por_semestre = {
    2: [
        "Representación simbólica y angular del entorno",
        "Comunicación activa en inglés",
        "Relación entre compuestos orgánicos y el entorno",
        "Comunicación en los ámbitos escolar y profesional",
        "Emprendimiento e innovación",
        "Manejo de aplicaciones por medios digitales",
        "Desarrollo de pensamiento computacional",
        "Identificación de redes de computadoras",
        "Implementación de interfaces de programación"
    ],
    4: [
        "Análisis derivativo de funciones",
        "Comunicación productiva en inglés",
        "Interpretación de fenómenos físicos de la materia",
        "Desarrollo ciudadano",
        "Desarrollo ágil de sistemas",
        "Aplicación de protocolos de datos",
        "Aplicación de modelos ETL",
        "Análisis de tendencias en datos"
    ],
    6: [
        "Tratamiento de datos y azar",
        "Interpretación de normas de convivencia ambiental",
        "Filosofía",
        "Aplicación de modelos predictivos",
        "Presentación y análisis prescriptivo de los datos",
        "Análisis del lenguaje natural",
        "Gestión de rendimiento de los datos"
    ]
}

matriculas = [str(1001 + i) for i in range(100)]
semestres = [2, 4, 6]
datos = []

for matricula in matriculas:
    semestre = random.choice(semestres)
    registro = {'MATRICULA': matricula, 'SEMESTRE': semestre}
    
    for materia in materias_por_semestre[semestre]:
        registro[materia] = random.choices(
            population = [random.randint(0, 59), random.randint(60, 100)],
            weights = [0.1, 0.9],
            k = 1
        )[0]
    
    datos.append(registro)

todas_materias = []
for semestre in [2, 4, 6]:
    todas_materias.extend(materias_por_semestre[semestre])

# Crear directorio si no existe
os.makedirs("tmp", exist_ok=True)

# Escribir el archivo CSV original
with open(r'tmp\calificaciones.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    campos = ['MATRICULA', 'SEMESTRE'] + todas_materias
    writer = csv.DictWriter(csvfile, fieldnames=campos)
    writer.writeheader()
    for registro in datos:
        writer.writerow(registro)

print("Archivo original 'calificaciones.csv' generado exitosamente!")

# === Parte 2: Cargar y ensuciar internamente ===

# Cargar el CSV generado en un DataFrame
df = pd.read_csv(r'tmp\calificaciones.csv', encoding='utf-8-sig')

# Identificar columnas de materias (todas excepto MATRICULA y SEMESTRE)
materias_cols = [col for col in df.columns if col not in ['MATRICULA', 'SEMESTRE']]

# Calcular número de registros a ensuciar (1%)
num_registros = len(df)
num_ensuciar = max(1, int(num_registros * 0.01))  # Al menos 1 registro

# Seleccionar registros aleatorios para ensuciar
registros_ensuciar = np.random.choice(df.index, size=num_ensuciar, replace=False)

# Procesar cada registro seleccionado
for idx in registros_ensuciar:
    # Seleccionar aproximadamente el 1% de las materias para modificar
    num_materias_modificar = max(1, int(len(materias_cols) * 0.01))
    materias_modificar = random.sample(materias_cols, num_materias_modificar)
    
    for materia in materias_modificar:
        # Seleccionar aleatoriamente una operación de ensuciado
        operacion = random.choice(['multiplicar', 'dividir'])
        
        if operacion == 'multiplicar':
            # Multiplicar por 100
            df.at[idx, materia] = df.at[idx, materia] * 100
        elif operacion == 'dividir':
            # Dividir entre 100
            df.at[idx, materia] = df.at[idx, materia] / 100

# === Parte 3: Muestreo aleatorio y exportación múltiple ===

# Mezclar el DataFrame ensuciado
df_muestreo = df.sample(frac=1, random_state=42).reset_index(drop=True)
total_filas = len(df_muestreo)

# Dividir en tres partes aproximadamente iguales
tam_parte = total_filas // 3
partes = [
    df_muestreo.iloc[:tam_parte],
    df_muestreo.iloc[tam_parte:2*tam_parte],
    df_muestreo.iloc[2*tam_parte:]
]

# Crear directorios necesarios
os.makedirs("data/calificaciones", exist_ok=True)

# Función para sanitizar nombres XML
def sanitize_xml_name(name):
    # Reemplazar caracteres especiales y espacios por guiones bajos
    sanitized = re.sub(r'[^\w]', '_', name)
    # Asegurar que no empiece con número
    if re.match(r'^\d', sanitized):
        sanitized = 'm_' + sanitized
    return sanitized

# 1. Exportar primera parte como CSV
partes[0].to_csv(r'data/calificaciones/calificaciones.csv', index=False, encoding='utf-8-sig')

# 2. Exportar segunda parte como JSON
partes[1].to_json(r'data/calificaciones/calificaciones.json', orient='records', indent=4, force_ascii=False)

# 3. Exportar tercera parte como XML (con sanitización de nombres)
df_xml = partes[2].copy()

# Sanitizar nombres de columnas para XML
nuevos_nombres = {col: sanitize_xml_name(col) for col in df_xml.columns}
df_xml.rename(columns=nuevos_nombres, inplace=True)

# Construir XML manualmente para mayor control
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<calificaciones>\n'

for _, row in df_xml.iterrows():
    xml_content += '  <registro>\n'
    for col_name, value in row.items():
        xml_content += f'    <{col_name}>'
        
        # Manejar diferentes tipos de datos
        if pd.isna(value):
            xml_content += ''
        elif isinstance(value, (int, float)):
            xml_content += str(value)
        else:
            # Escapar caracteres especiales para XML
            if isinstance(value, str):
                value = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            xml_content += str(value)
        
        xml_content += f'</{col_name}>\n'
    xml_content += '  </registro>\n'

xml_content += '</calificaciones>'

# Guardar XML con codificación UTF-8
with open(r'data/calificaciones/calificaciones.xml', 'w', encoding='utf-8') as xml_file:
    xml_file.write(xml_content)

print("Proceso completado exitosamente!")
print("Archivos generados:")
print(f"- CSV original: csv{os.sep}calificaciones.csv")
print(f"- Muestra CSV: data{os.sep}calificaciones{os.sep}calificaciones.csv")
print(f"- Muestra JSON: data{os.sep}calificaciones{os.sep}calificaciones.json")
print(f"- Muestra XML: data{os.sep}calificaciones{os.sep}calificaciones.xml")