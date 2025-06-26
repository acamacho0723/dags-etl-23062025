import pandas as pd
import numpy as np

# Diccionario de materias por semestre
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

# Obtener todas las materias
todas_materias = []
for sem, materias in materias_por_semestre.items():
    todas_materias.extend(materias)

# Cargar el CSV consolidado
df = pd.read_csv('data/consolidado/datos_consolidados.csv')

# Filtrar columnas relevantes
columnas_demograficas = [
    'MATRICULA', 'NOMBRE', 'APELLIDO_PATERNO', 'APELLIDO_MATERNO',
    'GENERO', 'FECHA_NACIMIENTO', 'NACIONALIDAD', 'SEMESTRE',
    'PROMEDIO', 'RIESGO_REPROBACION'
]

# Separar la fila de promedios de materias
df_prom_materia = df[df['MATRICULA'] == 'PROMEDIO_MATERIA']
df_alumnos = df[df['MATRICULA'] != 'PROMEDIO_MATERIA']

# Construir DIM_MATERIA
data_materia = []
for materia in todas_materias:
    if materia in df_prom_materia.columns:
        data_materia.append({
            'nombre_materia': materia,
            'PROMEDIO_MATERIA': df_prom_materia[materia].values[0]
        })
df_dim_materia = pd.DataFrame(data_materia)
df_dim_materia['materia_id'] = range(1, len(df_dim_materia) + 1)

# MODIFICACIÓN 1: Redondear PROMEDIO_MATERIA
df_dim_materia['PROMEDIO_MATERIA'] = df_dim_materia['PROMEDIO_MATERIA'].round(2)

# Construir DIM_ASISTENCIAS
df_dim_asistencias = df_alumnos[[
    'MATRICULA', 'SEMESTRE', 
    'TOTAL_ASISTENCIAS', 'TOTAL_INASISTENCIAS', 'PORCENTAJE_ASISTENCIA'
]].copy()
df_dim_asistencias = df_dim_asistencias.drop_duplicates()

# MODIFICACIÓN 2: Convertir asistencias a enteros y redondear porcentaje
df_dim_asistencias['TOTAL_ASISTENCIAS'] = df_dim_asistencias['TOTAL_ASISTENCIAS'].astype(int)
df_dim_asistencias['TOTAL_INASISTENCIAS'] = df_dim_asistencias['TOTAL_INASISTENCIAS'].astype(int)
df_dim_asistencias['PORCENTAJE_ASISTENCIA'] = df_dim_asistencias['PORCENTAJE_ASISTENCIA'].round(2)

# Construir HECHOS_DEMOGRAFICOS en formato largo
df_hechos = df_alumnos.melt(
    id_vars=columnas_demograficas,
    value_vars=todas_materias,
    var_name='nombre_materia',
    value_name='PORCENTAJE'
)

# MODIFICACIÓN 3: Redondear promedios y porcentajes
df_hechos['PROMEDIO'] = df_hechos['PROMEDIO'].round(2)
df_hechos['PORCENTAJE'] = df_hechos['PORCENTAJE'].round(2)

# Mapear nombre_materia a materia_id
map_materia_id = dict(zip(df_dim_materia['nombre_materia'], df_dim_materia['materia_id']))
df_hechos['materia_id'] = df_hechos['nombre_materia'].map(map_materia_id)
df_hechos = df_hechos.drop(columns=['nombre_materia'])

# Convertir fecha y booleano
df_hechos['FECHA_NACIMIENTO'] = pd.to_datetime(
    df_hechos['FECHA_NACIMIENTO'], 
    format='%d/%m/%Y',
    errors='coerce'
)
df_hechos['FECHA_NACIMIENTO'] = df_hechos['FECHA_NACIMIENTO'].apply(
    lambda x: x.strftime('%Y-%m-%d') if not pd.isna(x) else None
)
df_hechos['RIESGO_REPROBACION'] = df_hechos['RIESGO_REPROBACION'].astype(int)

# Reemplazar NaN en porcentajes por None
df_hechos['PORCENTAJE'] = df_hechos['PORCENTAJE'].replace({np.nan: None})

# Generar script SQL
with open('cubo_escolar.sql', 'w', encoding='utf-8') as f:
    # Crear base de datos y tablas
    f.write("""
SET FOREIGN_KEY_CHECKS=0;

-- Tabla DIM_MATERIA
CREATE TABLE DIM_MATERIA (
    materia_id INT PRIMARY KEY,
    nombre_materia VARCHAR(255) NOT NULL,
    PROMEDIO_MATERIA DECIMAL(5,2) NOT NULL
);

-- Tabla DIM_ASISTENCIAS
CREATE TABLE DIM_ASISTENCIAS (
    MATRICULA VARCHAR(50) NOT NULL,
    SEMESTRE INT NOT NULL,
    TOTAL_ASISTENCIAS INT NOT NULL,
    TOTAL_INASISTENCIAS INT NOT NULL,
    PORCENTAJE_ASISTENCIA DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (MATRICULA, SEMESTRE)
);

-- Tabla HECHOS_DEMOGRAFICOS
CREATE TABLE HECHOS_DEMOGRAFICOS (
    MATRICULA VARCHAR(50) NOT NULL,
    SEMESTRE INT NOT NULL,
    materia_id INT NOT NULL,
    NOMBRE VARCHAR(100) NOT NULL,
    APELLIDO_PATERNO VARCHAR(100),
    APELLIDO_MATERNO VARCHAR(100),
    GENERO VARCHAR(20),
    FECHA_NACIMIENTO DATE,
    NACIONALIDAD VARCHAR(50),
    PORCENTAJE DECIMAL(5,2),
    PROMEDIO DECIMAL(5,2) NOT NULL,
    RIESGO_REPROBACION BOOLEAN NOT NULL,
    PRIMARY KEY (MATRICULA, SEMESTRE, materia_id),
    FOREIGN KEY (materia_id) REFERENCES DIM_MATERIA(materia_id),
    FOREIGN KEY (MATRICULA, SEMESTRE) REFERENCES DIM_ASISTENCIAS(MATRICULA, SEMESTRE)
);

""")
    
    # Insertar DIM_MATERIA
    f.write("INSERT INTO DIM_MATERIA (materia_id, nombre_materia, PROMEDIO_MATERIA) VALUES\n")
    for i, row in df_dim_materia.iterrows():
        # Escapar comillas en nombres de materias
        nombre_materia = row['nombre_materia'].replace("'", "''")
        f.write(f"({row['materia_id']}, '{nombre_materia}', {row['PROMEDIO_MATERIA']})")
        f.write(",\n" if i < len(df_dim_materia)-1 else ";\n\n")
    
    # Insertar DIM_ASISTENCIAS
    f.write("INSERT INTO DIM_ASISTENCIAS (MATRICULA, SEMESTRE, TOTAL_ASISTENCIAS, TOTAL_INASISTENCIAS, PORCENTAJE_ASISTENCIA) VALUES\n")
    for i, row in df_dim_asistencias.iterrows():
        matricula = str(row['MATRICULA']).replace("'", "''")
        values = f"('{matricula}', {int(row['SEMESTRE'])}, {row['TOTAL_ASISTENCIAS']}, {row['TOTAL_INASISTENCIAS']}, {row['PORCENTAJE_ASISTENCIA']})"
        f.write(values)
        f.write(",\n" if i < len(df_dim_asistencias)-1 else ";\n\n")
    
    # Insertar HECHOS_DEMOGRAFICOS
    f.write("INSERT INTO HECHOS_DEMOGRAFICOS (MATRICULA, SEMESTRE, materia_id, NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, GENERO, FECHA_NACIMIENTO, NACIONALIDAD, PORCENTAJE, PROMEDIO, RIESGO_REPROBACION) VALUES\n")
    
    n = 1000  # Tamaño del bloque
    total_filas = len(df_hechos)
    
    for start in range(0, total_filas, n):
        end = min(start + n, total_filas)
        bloque = df_hechos.iloc[start:end]
        block_lines = []
        
        for _, row in bloque.iterrows():
            # Escapar caracteres especiales
            matricula = str(row['MATRICULA']).replace("'", "''")
            nombre = str(row['NOMBRE']).replace("'", "''")
            ap_paterno = str(row['APELLIDO_PATERNO']).replace("'", "''")
            ap_materno = str(row['APELLIDO_MATERNO']).replace("'", "''")
            genero = str(row['GENERO']).replace("'", "''")
            nacionalidad = str(row['NACIONALIDAD']).replace("'", "''")
            
            # Manejar valores nulos
            fecha_nac = f"'{row['FECHA_NACIMIENTO']}'" if row['FECHA_NACIMIENTO'] is not None else 'NULL'
            
            # Manejo especial para PORCENTAJE (None como NULL)
            if row['PORCENTAJE'] is None:
                porcentaje = 'NULL'
            else:
                porcentaje = f"{row['PORCENTAJE']:.2f}"
            
            # Convertir semestre a entero
            semestre = int(row['SEMESTRE'])
            
            # Construir línea
            values = (
                f"('{matricula}', {semestre}, {row['materia_id']}, "
                f"'{nombre}', '{ap_paterno}', '{ap_materno}', "
                f"'{genero}', {fecha_nac}, '{nacionalidad}', "
                f"{porcentaje}, {row['PROMEDIO']:.2f}, {row['RIESGO_REPROBACION']})"
            )
            block_lines.append(values)
        
        # Unir todas las líneas del bloque con comas
        f.write(",\n".join(block_lines))
        
        # Manejar el final del bloque
        if end < total_filas:
            f.write(";\n\nINSERT INTO HECHOS_DEMOGRAFICOS (MATRICULA, SEMESTRE, materia_id, NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, GENERO, FECHA_NACIMIENTO, NACIONALIDAD, PORCENTAJE, PROMEDIO, RIESGO_REPROBACION) VALUES\n")
        else:
            f.write(";\n")
    
    f.write("\nSET FOREIGN_KEY_CHECKS=1;")

print("Script SQL generado exitosamente: cubo_escolar.sql")