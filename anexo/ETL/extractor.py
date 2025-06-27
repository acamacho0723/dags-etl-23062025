import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

# Configuración de rutas
PATHS = {
    'asistencia': 'data/asistencia',
    'calificaciones': 'data/calificaciones',
    'datos_demograficos': 'data/datos_demograficos'
}

# Listas de nombres para corrección de género
NOMBRES_FEMENINOS = [
    'María', 'Ana', 'Sofía', 'Lucía', 'Valentina', 'Camila', 'Ximena', 'Renata',
    'Daniela', 'Gabriela', 'Victoria', 'Isabella', 'Paula', 'Alejandra', 'Fernanda'
]

NOMBRES_MASCULINOS = [
    'Juan', 'Luis', 'Carlos', 'José', 'Miguel', 'Jorge', 'Diego', 'Manuel',
    'Pedro', 'Ricardo', 'Francisco', 'Andrés', 'Antonio', 'Rafael', 'Alejandro'
]

# Materias por semestre
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

# =====================================================
# Funciones para cargar datos desde diferentes formatos
# =====================================================

def cargar_csv(ruta):
    return pd.read_csv(ruta, encoding='utf-8-sig')

def cargar_json(ruta):
    return pd.read_json(ruta, encoding='utf-8')

def cargar_xml(ruta):
    try:
        return pd.read_xml(ruta)
    except:
        # Manejo manual de XML si falla la carga estándar
        with open(ruta, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Extraer registros
        registros = re.findall(r'<registro>(.*?)</registro>', xml_content, re.DOTALL)
        datos = []
        
        for reg in registros:
            fila = {}
            campos = re.findall(r'<([^>]+)>(.*?)</\1>', reg, re.DOTALL)
            for campo, valor in campos:
                fila[campo] = valor.strip()
            datos.append(fila)
        
        return pd.DataFrame(datos)

def cargar_dataset(tipo):
    """Carga todos los archivos de un dataset, elimina duplicados y maneja valores vacíos"""
    dfs = []
    for formato in ['csv', 'json', 'xml']:
        ruta = os.path.join(PATHS[tipo], f"{tipo}.{formato}")
        if os.path.exists(ruta):
            if formato == 'csv':
                df_temp = cargar_csv(ruta)
            elif formato == 'json':
                df_temp = cargar_json(ruta)
            elif formato == 'xml':
                df_temp = cargar_xml(ruta)
                
                # Corrección específica para nombres de columnas en XML
                if tipo == 'calificaciones':
                    # Revertir sanitización: guiones bajos a espacios
                    new_columns = {}
                    for col in df_temp.columns:
                        if col not in ['MATRICULA', 'SEMESTRE']:
                            new_columns[col] = col.replace('_', ' ')
                        else:
                            new_columns[col] = col
                    df_temp = df_temp.rename(columns=new_columns)
                
                elif tipo == 'asistencia':
                    # Remover guión bajo inicial y mantener formato de fecha
                    new_columns = {}
                    for col in df_temp.columns:
                        if col != 'MATRICULA':
                            new_columns[col] = col.lstrip('_')
                        else:
                            new_columns[col] = col
                    df_temp = df_temp.rename(columns=new_columns)
            
            # Manejar valores None y NaN
            df_temp = df_temp.fillna('')
            dfs.append(df_temp)
    
    if dfs:
        # Combinar todos los DataFrames
        df = pd.concat(dfs, ignore_index=True)
        
        # Eliminar duplicados
        df = df.drop_duplicates()
        
        # Eliminar filas completamente vacías
        df = df.dropna(how='all')
        
        return df
    return pd.DataFrame()

# =====================================================
# Funciones de corrección de datos
# =====================================================

def inferir_genero(nombre):
    """Infiere el género basado en listas de nombres"""
    nombre = str(nombre).strip()
    if nombre in NOMBRES_FEMENINOS:
        return 'F'
    elif nombre in NOMBRES_MASCULINOS:
        return 'M'
    return ''

def formatear_fecha(fecha_str):
    """Intenta convertir una cadena de fecha al formato dd/mm/YYYY"""
    if not fecha_str or fecha_str in ['None', 'nan', '']:
        return None
    
    # Limpiar caracteres no deseados (guiones bajos, espacios, etc.)
    fecha_limpia = re.sub(r'[^0-9/]', '', str(fecha_str))
    
    # Intentar parsear la fecha en diferentes formatos
    formatos_posibles = [
        '%d/%m/%Y',  # Formato esperado
        '%Y/%m/%d',  # Formato ISO
        '%m/%d/%Y',  # Formato americano
        '%d%m%Y',    # Sin separadores
        '%Y%m%d'     # Formato ISO sin separadores
    ]
    
    for formato in formatos_posibles:
        try:
            fecha_dt = datetime.strptime(fecha_limpia, formato)
            return fecha_dt.strftime('%d/%m/%Y')
        except ValueError:
            continue
    
    # Si ninguno funcionó, devolver la fecha limpia (podría no estar formateada)
    return fecha_limpia

def corregir_asistencias(df):
    """Correcciones para el dataset de asistencias"""
    # Identificar columnas de fechas (todas excepto MATRICULA)
    columnas_fecha = [col for col in df.columns if col != 'MATRICULA']
    
    # Convertir S/N a booleanos (True/False)
    for col in columnas_fecha:
        # Convertir a string y limpiar valores
        df[col] = df[col].astype(str).str.strip().str.upper()
        
        # Aplicar reglas de corrección
        df[col] = np.where(
            df[col].isin(['S', '1', 'TRUE', 'T']), 
            True, 
            np.where(
                df[col].isin(['N', '0', 'FALSE', 'F']),
                False,
                False  # Cualquier otro valor se considera ausente
            )
        )
    
    return df

def corregir_calificaciones(df_calif):
    """Correcciones para el dataset de calificaciones"""
    # Verificar y corregir columna SEMESTRE
    if 'SEMESTRE' not in df_calif.columns:
        df_calif['SEMESTRE'] = 2
    
    # Convertir SEMESTRE a numérico y manejar errores
    df_calif['SEMESTRE'] = pd.to_numeric(df_calif['SEMESTRE'], errors='coerce')
    # Rellenar valores faltantes con 2 y convertir a entero
    df_calif['SEMESTRE'] = df_calif['SEMESTRE'].fillna(2).astype(int)
    # Forzar semestres válidos (2,4,6)
    df_calif['SEMESTRE'] = df_calif['SEMESTRE'].apply(
        lambda x: x if x in {2, 4, 6} else 2
    )
    
    # Identificar columnas de materias
    materias_df = [col for col in df_calif.columns if col not in ['MATRICULA', 'SEMESTRE']]
    
    # 1. Convertir todas las materias a numérico
    for materia in materias_df:
        df_calif[materia] = pd.to_numeric(df_calif[materia], errors='coerce')
    
    # 2. Eliminar calificaciones de materias no correspondientes al semestre
    for idx, row in df_calif.iterrows():
        semestre = row['SEMESTRE']
        materias_validas = materias_por_semestre.get(semestre, [])
        
        for materia in materias_df:
            if materia not in materias_validas:
                df_calif.at[idx, materia] = np.nan
    
    # 3. Calcular promedios por alumno (solo materias válidas)
    promedios_alumno = {}
    for matricula, group in df_calif.groupby('MATRICULA'):
        # Obtener semestre del grupo (todos deberían ser iguales)
        semestre = group['SEMESTRE'].iloc[0]
        materias_validas = materias_por_semestre.get(semestre, [])
        
        # Filtrar solo materias válidas presentes en el DataFrame
        materias_calculo = [m for m in materias_validas if m in group.columns]
        valores_validos = group[materias_calculo].values.flatten()
        valores_validos = valores_validos[~np.isnan(valores_validos)]
        valores_validos = valores_validos[(valores_validos >= 1) & (valores_validos <= 100)]
        
        if len(valores_validos) > 0:
            promedios_alumno[matricula] = np.mean(valores_validos)
        else:
            promedios_alumno[matricula] = 70.0  # Valor predeterminado
    
    # 4. Reemplazar valores anormales en materias válidas
    def corregir_valor_materia(row, materia):
        valor = row[materia]
        # Solo corregir si es materia válida para el semestre
        semestre = row['SEMESTRE']
        materias_validas = materias_por_semestre.get(semestre, [])
        
        if materia not in materias_validas:
            return np.nan
        
        # Verificar si el valor es anormal
        if pd.isna(valor) or valor < 1 or valor > 100:
            return promedios_alumno[row['MATRICULA']]
        return valor
    
    for materia in materias_df:
        df_calif[materia] = df_calif.apply(
            lambda row: corregir_valor_materia(row, materia), 
            axis=1
        )
    
    # Agregar columna de promedio
    df_calif['PROMEDIO'] = df_calif['MATRICULA'].map(promedios_alumno)
    
    return df_calif

def corregir_datos_demograficos(df_demo, df_calif):
    """Correcciones para el dataset demográfico"""
    # Obtener semestre de calificaciones
    df_demo = df_demo.merge(
        df_calif[['MATRICULA', 'SEMESTRE']], 
        on='MATRICULA', 
        how='left'
    )
    
    # 1. Corregir nombres vacíos
    # Si el nombre está vacío, usar 'Alumno' o 'Alumna' basado en el género
    df_demo['NOMBRE'] = df_demo.apply(
        lambda x: 'Alumna' if x['GENERO'] == 'F' else 'Alumno'
        if pd.isna(x['NOMBRE']) or x['NOMBRE'] == '' else x['NOMBRE'],
        axis=1
    )
    
    # 2. Corregir género vacío
    # Primero intentar inferir del nombre
    df_demo['GENERO_CORREGIDO'] = df_demo.apply(
        lambda x: inferir_genero(x['NOMBRE']) 
        if pd.isna(x['GENERO']) or x['GENERO'] == '' else x['GENERO'],
        axis=1
    )
    
    # Si aún está vacío, establecer 'M' como predeterminado
    df_demo['GENERO_CORREGIDO'] = df_demo['GENERO_CORREGIDO'].replace('', 'M')
    df_demo['GENERO_CORREGIDO'] = df_demo['GENERO_CORREGIDO'].fillna('M')
    
    # 3. Corregir fechas de nacimiento vacías o inválidas
    def corregir_fecha_nacimiento(row):
        fecha = str(row['FECHA_NACIMIENTO']).strip()
        if not fecha or fecha == 'None' or fecha == 'nan':
            semestre = row['SEMESTRE']
            if semestre == 2:
                return '01/01/2009'
            elif semestre == 4:
                return '01/01/2008'
            else:  # semestre 6
                return '01/01/2007'
        return fecha
    
    # Primero aplicar la corrección básica
    df_demo['FECHA_NACIMIENTO_CORREGIDA'] = df_demo.apply(
        corregir_fecha_nacimiento, 
        axis=1
    )
    
    # Luego formatear todas las fechas al formato dd/mm/YYYY
    df_demo['FECHA_NACIMIENTO_CORREGIDA'] = df_demo['FECHA_NACIMIENTO_CORREGIDA'].apply(formatear_fecha)
    
    # Para las fechas que aún no se pudieron formatear, usar valores predeterminados por semestre
    mascara_fecha_invalida = df_demo['FECHA_NACIMIENTO_CORREGIDA'].isna()
    df_demo.loc[mascara_fecha_invalida, 'FECHA_NACIMIENTO_CORREGIDA'] = df_demo[mascara_fecha_invalida].apply(
        lambda row: '01/01/2009' if row['SEMESTRE'] == 2 else
                   '01/01/2008' if row['SEMESTRE'] == 4 else
                   '01/01/2007',
        axis=1
    )
    
    # 4. Eliminar columna TITULO si existe
    if 'TITULO' in df_demo.columns:
        df_demo = df_demo.drop(columns=['TITULO'])
    
    # Seleccionar y renombrar columnas finales
    df_demo = df_demo[[
        'MATRICULA', 'NOMBRE', 'APELLIDO_PATERNO', 'APELLIDO_MATERNO', 
        'GENERO_CORREGIDO', 'FECHA_NACIMIENTO_CORREGIDA', 'NACIONALIDAD', 'SEMESTRE'
    ]].rename(columns={
        'GENERO_CORREGIDO': 'GENERO',
        'FECHA_NACIMIENTO_CORREGIDA': 'FECHA_NACIMIENTO'
    })
    
    return df_demo

# =====================================================
# Procesamiento principal
# =====================================================

def main():
    # Cargar todos los datasets
    print("Cargando datos de asistencias...")
    df_asistencias = cargar_dataset('asistencia')
    
    print("Cargando datos de calificaciones...")
    df_calificaciones = cargar_dataset('calificaciones')
    
    print("Cargando datos demográficos...")
    df_demograficos = cargar_dataset('datos_demograficos')
    
    # Aplicar correcciones
    print("Aplicando correcciones a asistencias...")
    df_asistencias_corregidas = corregir_asistencias(df_asistencias)
    
    print("Aplicando correcciones a calificaciones...")
    df_calificaciones_corregidas = corregir_calificaciones(df_calificaciones)
    
    print("Aplicando correcciones a datos demográficos...")
    df_demograficos_corregidos = corregir_datos_demograficos(
        df_demograficos, 
        df_calificaciones_corregidas
    )
    
    # Combinar todos los datos
    print("Combinando datasets...")
    # Primero combinar datos demográficos con calificaciones
    df_temp = pd.merge(
        df_demograficos_corregidos,
        df_calificaciones_corregidas,
        on=['MATRICULA', 'SEMESTRE'],
        how='inner'
    )
    
    # Luego combinar con asistencias
    df_final = pd.merge(
        df_temp,
        df_asistencias_corregidas,
        on='MATRICULA',
        how='inner'
    )
    
    # Eliminar posibles duplicados restantes
    df_final = df_final.drop_duplicates(subset='MATRICULA')
    
    # Calcular nuevas métricas
    print("Calculando nuevas métricas...")
    
    # Obtener columnas de asistencia (fechas)
    columnas_asistencia = [col for col in df_asistencias_corregidas.columns if col != 'MATRICULA']
    total_dias = len(columnas_asistencia)
    
    # 1. Calcular total de asistencias (suma de True)
    df_final['TOTAL_ASISTENCIAS'] = df_final[columnas_asistencia].sum(axis=1)
    
    # 2. Calcular total de inasistencias
    df_final['TOTAL_INASISTENCIAS'] = total_dias - df_final['TOTAL_ASISTENCIAS']
    
    # 3. Calcular porcentaje de asistencias
    df_final['PORCENTAJE_ASISTENCIA'] = (df_final['TOTAL_ASISTENCIAS'] / total_dias) * 100
    
    # 4. Calcular riesgo de reprobación (asistencia <70% y promedio <80)
    df_final['RIESGO_REPROBACION'] = (df_final['PORCENTAJE_ASISTENCIA'] < 70) & (df_final['PROMEDIO'] < 80)
    
    # 5. Calcular promedio por materia
    print("Calculando promedio por materia...")
    # Identificar todas las materias posibles
    todas_las_materias = set()
    for semestre, materias in materias_por_semestre.items():
        todas_las_materias.update(materias)
    
    # Filtrar solo las materias que están en el df_final
    columnas_materias = [m for m in todas_las_materias if m in df_final.columns]
    
    # Calcular el promedio de cada materia (ignorando NaN)
    promedios_materia = {}
    for materia in columnas_materias:
        promedios_materia[materia] = df_final[materia].mean(skipna=True)
    
    # Crear una nueva fila con el identificador y los promedios
    nueva_fila = {'MATRICULA': 'PROMEDIO_MATERIA'}
    # Agregar los promedios de cada materia
    for materia in columnas_materias:
        nueva_fila[materia] = promedios_materia[materia]
    
    # Convertir a DataFrame
    df_nueva_fila = pd.DataFrame([nueva_fila])
    
    # Asegurar que tiene todas las columnas de df_final (rellenando NaN para las que no están en nueva_fila)
    df_nueva_fila = df_nueva_fila.reindex(columns=df_final.columns, fill_value=np.nan)
    
    # Concatenar al final
    df_final = pd.concat([df_final, df_nueva_fila], ignore_index=True)
    
    # Guardar resultado consolidado
    os.makedirs('data/consolidado', exist_ok=True)
    ruta_final = 'data/consolidado/datos_consolidados.csv'
    df_final.to_csv(ruta_final, index=False, encoding='utf-8-sig')
    
    print("\nProceso completado exitosamente!")
    print(f"Datos consolidados guardados en: {ruta_final}")
    print(f"Total de registros procesados: {len(df_final)}")
    print(f"Total de columnas: {len(df_final.columns)}")
    print(f"Matrículas únicas: {df_final['MATRICULA'].nunique() - 1}")  # Restar 1 por la fila de promedio

if __name__ == "__main__":
    main()