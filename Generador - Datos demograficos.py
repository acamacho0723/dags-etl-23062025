import pandas as pd
import numpy as np
import os
import re
import random

# === Configuración inicial ===
# Crear directorios necesarios
os.makedirs("tmp", exist_ok=True)
os.makedirs("data/datos_demograficos", exist_ok=True)

# === Leer archivo base ===
# Leer el archivo calificaciones.csv para obtener matrículas y semestres
df_base = pd.read_csv(r'tmp/calificaciones.csv', encoding='utf-8-sig')
# Conservar solo las columnas necesarias
df_base = df_base[['MATRICULA', 'SEMESTRE']]

# === Configuración para datos demográficos ===
nombres_femeninos = [
    'María', 'Ana', 'Sofía', 'Lucía', 'Valentina', 'Camila', 'Ximena', 'Renata',
    'Daniela', 'Gabriela', 'Victoria', 'Isabella', 'Paula', 'Alejandra', 'Fernanda'
]

nombres_masculinos = [
    'Juan', 'Luis', 'Carlos', 'José', 'Miguel', 'Jorge', 'Diego', 'Manuel',
    'Pedro', 'Ricardo', 'Francisco', 'Andrés', 'Antonio', 'Rafael', 'Alejandro'
]

apellidos = [
    'García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'Pérez', 'González',
    'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Díaz', 'Vázquez', 'Castro', 'Ruiz',
    'Jiménez', 'Mendoza', 'Álvarez', 'Romero', 'Navarro', 'Morales', 'Ortega'
]

paises = {
    'MX': 'Mexicana',
    'US': 'Estadounidense',
    'ES': 'Española',
    'CO': 'Colombiana',
    'AR': 'Argentina',
    'CL': 'Chilena',
    'PE': 'Peruana',
    'EC': 'Ecuatoriana',
    'GT': 'Guatemalteca',
    'CU': 'Cubana'
}

# === Generar datos demográficos ===
datos = []

for _, row in df_base.iterrows():
    matricula = row['MATRICULA']
    semestre = row['SEMESTRE']
    
    # Determinar género y nombre
    genero = random.choice(['F', 'M'])
    if genero == 'F':
        nombre = random.choice(nombres_femeninos)
    else:
        nombre = random.choice(nombres_masculinos)
    
    # Generar apellidos
    apellido_paterno = random.choice(apellidos)
    apellido_materno = random.choice(apellidos)
    
    # Calcular fecha de nacimiento según semestre
    if semestre == 2:
        año_nacimiento = 2009
    elif semestre == 4:
        año_nacimiento = 2008
    else:  # semestre 6
        año_nacimiento = 2007
    
    # Generar mes y día aleatorios
    mes_nacimiento = random.randint(1, 12)
    # Determinar días máximos por mes
    if mes_nacimiento == 2:
        max_dias = 28
    elif mes_nacimiento in [4, 6, 9, 11]:
        max_dias = 30
    else:
        max_dias = 31
    
    dia_nacimiento = random.randint(1, max_dias)
    fecha_nacimiento = f"{dia_nacimiento:02d}/{mes_nacimiento:02d}/{año_nacimiento}"
    
    # Seleccionar nacionalidad
    nacionalidad = random.choice(list(paises.values()))
    
    # Crear registro
    registro = {
        'MATRICULA': matricula,
        'NOMBRE': nombre,
        'APELLIDO_PATERNO': apellido_paterno,
        'APELLIDO_MATERNO': apellido_materno,
        'GENERO': genero,
        'FECHA_NACIMIENTO': fecha_nacimiento,
        'NACIONALIDAD': nacionalidad
    }
    
    datos.append(registro)

# Crear DataFrame
df = pd.DataFrame(datos)

# === Ensuciar datos ===
# Campos a ensuciar
campos_ensuciar = ['NOMBRE', 'GENERO', 'FECHA_NACIMIENTO']

# Calcular número de registros a ensuciar (30%)
num_registros = len(df)
num_ensuciar = max(1, int(num_registros * 0.30))

# Seleccionar registros aleatorios para ensuciar
registros_ensuciar = np.random.choice(df.index, size=num_ensuciar, replace=False)

# Procesar cada registro seleccionado
for idx in registros_ensuciar:
    # Seleccionar aleatoriamente 1-3 campos para borrar
    num_campos_borrar = random.randint(1, 3)
    campos_borrar = random.sample(campos_ensuciar, num_campos_borrar)
    
    for campo in campos_borrar:
        df.at[idx, campo] = ''

# === Exportar a múltiples formatos ===
# Función para sanitizar nombres XML
def sanitize_xml_name(name):
    # Reemplazar caracteres especiales por guiones bajos
    sanitized = re.sub(r'[^\w]', '_', name)
    # Asegurar que no empiece con número
    if re.match(r'^\d', sanitized):
        sanitized = 'col_' + sanitized
    return sanitized

# 1. Exportar como CSV
df.to_csv(r'data/datos_demograficos/datos_demograficos.csv', index=False, encoding='utf-8-sig')

# 2. Exportar como JSON
df.to_json(r'data/datos_demograficos/datos_demograficos.json', orient='records', indent=4, force_ascii=False)

# 3. Exportar como XML
# Sanitizar nombres de columnas para XML
nuevos_nombres = {col: sanitize_xml_name(col) for col in df.columns}
df_xml = df.rename(columns=nuevos_nombres)

# Construir XML manualmente para mayor control
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<datos_demograficos>\n'

for _, row in df_xml.iterrows():
    xml_content += '  <registro>\n'
    for col_name, value in row.items():
        xml_content += f'    <{col_name}>'
        
        # Escapar caracteres especiales para XML
        if isinstance(value, str):
            value = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml_content += str(value)
        
        xml_content += f'</{col_name}>\n'
    xml_content += '  </registro>\n'

xml_content += '</datos_demograficos>'

# Guardar XML con codificación UTF-8
with open(r'data/datos_demograficos/datos_demograficos.xml', 'w', encoding='utf-8') as xml_file:
    xml_file.write(xml_content)

print("Proceso completado exitosamente!")
print("Archivos generados en 'data/datos_demograficos':")
print("- datos_demograficos.csv")
print("- datos_demograficos.json")
print("- datos_demograficos.xml")