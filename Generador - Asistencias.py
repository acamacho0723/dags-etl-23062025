import pandas as pd
import numpy as np
import os
import re

# 1. Generar lista de matrículas desde 1001 hasta 1100
matriculas = list(range(1001, 1101))

# 2. Generar el rango de fechas de lunes a viernes
fechas = pd.date_range(
    start="2025-02-17",
    end="2025-07-04",
    freq="B"  # 'B' = business days (excluye sábados y domingos)
)
# Formatear como dd/mm/YYYY
fechas_str = fechas.strftime("%d/%m/%Y")

# 3. Crear DataFrame vacío con índices = matrículas y columnas = fechas
df = pd.DataFrame(
    index=matriculas,
    columns=fechas_str
)

# 4. Rellenar asistencias de forma aleatoria (“S” o “N”)
np.random.seed(42)  # para reproducibilidad
df[:] = np.random.choice(
    ["S", "N"],
    size=(len(matriculas), len(fechas_str)),
    p = [0.7, 0.3]
)

# 5. Preparar para exportar: convertir el índice en columna “MATRICULA”
df.index.name = "MATRICULA"
df.reset_index(inplace=True)

# --- Nuevas modificaciones solicitadas ---

# A. Borrar un 1% de las asistencias (convertirlas a NaN)
num_filas, num_columnas = df.shape
total_celdas = num_filas * (num_columnas - 1)  # Excluye columna MATRICULA
num_celdas_borrar = int(total_celdas * 0.01)   # 1% del total

if num_celdas_borrar > 0:
    # Generar coordenadas aleatorias sin repetición
    filas_aleatorias = np.random.choice(num_filas, size=num_celdas_borrar, replace=False)
    # Columnas: excluyendo la primera (MATRICULA)
    columnas_aleatorias = np.random.choice(range(1, num_columnas), size=num_celdas_borrar, replace=False)
    
    for i in range(num_celdas_borrar):
        fila = filas_aleatorias[i]
        col = columnas_aleatorias[i]
        df.iat[fila, col] = np.nan

# Convertir todos los NaN a string vacío
df = df.fillna("")

# B. Renombrar columnas de fecha para formato válido (reemplazar / por -)
nuevas_columnas = ['MATRICULA'] + [fecha.replace('/', '-') for fecha in fechas_str]
df.columns = nuevas_columnas

# C. Crear directorio principal si no existe
os.makedirs("data/asistencia", exist_ok=True)

# D. Guardar en tres formatos diferentes (muestreo aleatorio)
# Mezclar el DataFrame
df_muestreo = df.sample(frac=1, random_state=42).reset_index(drop=True)
total_filas = len(df_muestreo)

# Dividir en tres partes aproximadamente iguales
tam_parte = total_filas // 3
partes = [
    df_muestreo.iloc[:tam_parte],
    df_muestreo.iloc[tam_parte:2*tam_parte],
    df_muestreo.iloc[2*tam_parte:]
]

# Función para crear nombres XML válidos
def make_valid_xml_name(col_name: str) -> str:
    # Si empieza por dígito, anteponemos '_'
    if re.match(r'^[0-9]', col_name):
        return "_" + col_name
    return col_name

# Procesar solo el DataFrame para XML
df_xml = partes[1].copy()

# Aplicar solo a las columnas de fecha (dejamos "MATRICULA" igual)
new_cols = []
for c in df_xml.columns:
    if c == "MATRICULA":
        new_cols.append(c)
    else:
        new_cols.append(make_valid_xml_name(c))
df_xml.columns = new_cols

# Guardar cada parte en diferente formato
partes[0].to_csv(r"data/asistencia/asistencia.csv", index=False, encoding="utf-8")
df_xml.to_xml(r"data/asistencia/asistencia.xml", index=False)
partes[2].to_json(r"data/asistencia/asistencia.json", orient="records", indent=4)

print("Proceso completado:")
print(f"- CSV guardado en: data/asistencia/asistencia.csv")
print(f"- XML guardado en: data/asistencia/asistencia.xml")
print(f"- JSON guardado en: data/asistencia/asistencia.json")