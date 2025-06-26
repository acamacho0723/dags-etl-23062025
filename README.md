---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.2
  kernelspec:
    display_name: base
    language: python
    name: python3
---

<img src = "media\Portada.jpg">


# Objetivo del trabajo


Desarrollar un prototipo de dashboard web interactivo que centralice y visualice esta información para que los coordinadores académicos puedan identificar patrones y áreas de oportunidad rápidamente.


# Metodología Ágil


Para la organización de nuestra actividad, hicimos uso de los siguientes elementos:


## User Story map


<img src = 'media\mi tablero de trello\tablero.png'>


<img src = 'media\mi tablero de trello\1.1.png'>


<img src = 'media\mi tablero de trello\1.15.png'>


<img src = 'media\mi tablero de trello\1.2.png' >


<img src = 'media\mi tablero de trello\1.25.png'>


<img src = 'media\Capturas Sprint Backlog\2.3.png'>


<img src = 'media\Capturas Sprint Backlog\2.4.png'>


<img src = 'media\Capturas Sprint Backlog\2.5.png'>


<img src ='media\Capturas Sprint Backlog\2.6.png'>


<img src = 'media\Capturas Sprint Backlog\2.7.png'>


## Sprint Backlog


<img src = 'media\Capturas Sprint Backlog\Tablero.png'>


## Product Backlog


<img src = 'media\Product Backlog\Tablero.png'>


# Creación de los datasets para el análisis


Para desarrollar nuestra actividad, requerimos de tres archivos csv que contengan:
1. Calificaciones
2. Asistencias
3. Datos demógraficos de los estudiantes

para mínimo 100 estudiantes. En nuestro equipo, decidimos centrarnos en estudiantes de una sola carrera, concretamente 
<strong>CDIA</strong>.

Con esto en mente, nos propusimos desarollar un código de python para cada uno de los datasets para nuestra actividad.


## Dataset de calificaciones


Con el fin de trabajar con diversos semestres, obtuvimos una lista de los módulos para cada uno de ellos, basándonos en la siguiente tabla:


<img src = "media\1. Mapa curricular.png">


###### Diagrama obtenido de <a href = "media\Mapa Curricular.pdf">Mapa Curricular CDIA</a>


Dado que estamos en la segunda mitad del año, usamos los semestres 2, 4 y 6. 

Las materias para <strong>2do semestre</strong> son:
1. Representación simbólica y angular del entorno
        
2. Comunicación activa en inglés
        
3. Relación entre compuestos orgánicos y el entorno
        
4. Comunicación en los ámbitos escolar y profesional
        
5. Emprendimiento e innovación
        
6. Manejo de aplicaciones por medios digitales
        
7. Desarrollo de pensamiento computacional
        
8. Identificación de redes de computadoras
        
9. Implementación de interfaces de programación

Las materias para <strong>4to semestre</strong> son:
1. Análisis derivativo de funciones

2. Comunicación productiva en inglés

3. Interpretación de fenómenos físicos de la materia

4. Desarrollo ciudadano

5. Desarrollo ágil de sistemas

6. Aplicación de protocolos de datos

7. Aplicación de modelos ETL

8. Análisis de tendencias en datos

Las materias para <strong>6to semestre</strong> son:
1. Tratamiento de datos y azar

2. Interpretación de normas de convivencia ambiental

3. Filosofía

4. Aplicación de modelos predictivos

5. Presentación y análisis prescriptivo de los datos

6. Análisis del lenguaje natural

7. Gestión de rendimiento de los datos

Se ensuciaron algunos registros de la siguiente manera:
- Multiplicar calificación por 100.

- Dividir calificación entre 100.

A partir de estos datos, desarrollamos un programa para generar el dataset, el cual podemos desenvolver en los siguientes pasos:


### 1. Generación del CSV original

<!-- #region -->
```python
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
```
<!-- #endregion -->

<strong>Importaciones</strong>

- `pandas`, `numpy`: Para manejo de datos.  

- `os`, `re`, `random`, `csv`: Para operaciones de sistema, expresiones regulares, generación aleatoria y escritura en CSV.

<strong>Definición de asignaturas</strong>

- El diccionario `materias_por_semestre` lista, para los semestres 2, 4 y 6, las materias que se van a calificar.

<strong>Generación de matrículas y datos aleatorios</strong>

- Se crean 100 matrículas (del <em>1001 al 1100</em>).  
- A cada alumno se le asigna aleatoriamente uno de los tres semestres disponibles.  
- Para cada materia correspondiente a ese semestre, se genera una <em>nota aleatoria entre 0 y 100, con 90% de probabilidad de que sea >=60</em>.  
- Cada registro se guarda en la lista `datos`.

<strong>Construcción de la lista completa de materias</strong>

- Se combinan todas las materias de los tres semestres en la lista `todas_materias`.

<strong>Creación de carpeta y escritura del CSV</strong>

- Se asegura que exista la carpeta `tmp`.  
- Se abre (o crea) el archivo `tmp\calificaciones.csv` con <em>codificación UTF-8 con BOM</em>.  
- Se escribe la cabecera y luego todas las filas de notas.


### 2. Carga del CSV y <i>ensuciamiento</i> de los datos

<!-- #region -->
```python
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
```
<!-- #endregion -->

<strong>Carga del CSV en un DataFrame de pandas</strong>

- Se carga el archivo CSV en un DataFrame de `pandas`.

<strong>Detección de columnas de nota</strong>

- Se identifican las columnas que contienen notas, descartando las columnas `MATRICULA` y `SEMESTRE`.

<strong>Cálculo del 10% de filas a «ensuciar»</strong>

- Se calcula el 10% del total de filas para alterarlas, asegurando un mínimo de 1.

<strong>Selección aleatoria de índices</strong>

- Se eligen aleatoriamente los índices de las filas que serán modificadas.

<strong>Modificación de las filas seleccionadas</strong>

- Para cada fila elegida:
  - Se selecciona un 30% de las materias para alterar.
  - Por cada materia seleccionada, se aplica aleatoriamente una de las siguientes operaciones:
    - Multiplicar la nota por 100.
    - Dividir la nota entre 100.
    - Borrar la nota (establecerla como `NaN`).

<strong>Reemplazo de NaN</strong>

- Finalmente, se reemplazan los valores `NaN` por cadenas vacías (`''`) para evitar problemas en exportaciones posteriores.


### 3. Muestreo y exportaciones múltiples

<!-- #region -->
```python
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
partes[1].to_json(
    r'data/calificaciones/calificaciones.json',
    orient='records',
    indent=4,
    force_ascii=False
)

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
                value = value.replace('&', '&amp;') \
                             .replace('<', '&lt;') \
                             .replace('>', '&gt;')
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
```
<!-- #endregion -->

<strong>Barajado y partición del DataFrame</strong>

- Se baraja todo el DataFrame sucio usando `.sample(frac=1)` y se reinician los índices.
- Luego se divide en 3 partes iguales (o lo más parecidas posible).

<strong>Creación de carpeta de salida</strong>

- Se crea la carpeta `data/calificaciones` si no existe.

<strong>Definición de <code>sanitize_xml_name()</code></strong>

- Esta función realiza:
  - Sustitución de espacios y caracteres no alfanuméricos por `_`.
  - Asegura que el nombre no comience con un dígito (agrega prefijo `m_` si es necesario).

<strong>Exportaciones</strong>

- `partes[0]` → CSV usando `.to_csv`.
- `partes[1]` → JSON usando `.to_json` con `force_ascii=False` para mantener acentos.
- `partes[2]` → XML manual:
  - Se copia el trozo y se renombran las columnas con `sanitize_xml_name()`.
  - Se construye una cadena XML con etiqueta raíz `<calificaciones>`.
  - Por cada fila, se agrega un nodo `<registro>` con cada campo.
  - Se escapan los caracteres especiales: `&`, `<`, `>` en los valores de texto.
  - El archivo se guarda en `data/calificaciones/calificaciones.xml`.


### 4. Ejecución del generador


Integramos todo lo anterior dentro de la siguiente celda y lo ejecutamos:

```python
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
```

y cargamos una muestra de cada uno de los datos de salida:

```python
pd.read_csv(r"data\calificaciones\calificaciones.csv").head()
```

```python
pd.read_json(r"data\calificaciones\calificaciones.json").head()
```

```python
pd.read_xml(r"data\calificaciones\calificaciones.xml").head()
```

## Dataset de asistencias


De la misma manera, nos propusimos crear el dataset de asistencias con una solución implementada en python. 

Se ensuciaron algunos registros, aplicando la siguiente regla:
- Borrar S o N (dejar registros vacíos).

El programa que utilizamos para este dataset se desarrolló en las etapas que mostramos a continuación:


### 1. Importación de librerías

<!-- #region -->
```python
import pandas as pd
import numpy as np
import os
import re
```
<!-- #endregion -->

<strong>Descripción de módulos usados</strong>

- <code>pandas</code> (<code>pd</code>): Manejo de tablas mediante estructuras <code>DataFrame</code>.

- <code>numpy</code> (<code>np</code>): Operaciones numéricas y generación aleatoria.

- <code>os</code>: Operaciones sobre el sistema de archivos, como crear carpetas.

- <code>re</code>: Expresiones regulares, utilizadas más adelante para validar nombres.


### 2. Generar lista de matrículas

<!-- #region -->
```python
# 1. Generar lista de matrículas desde 1001 hasta 1100
matriculas = list(range(1001, 1101))
```
<!-- #endregion -->

<strong>Generación de IDs de alumnos</strong>

- Se crea una lista de enteros del <code>1001</code> al <code>1100</code>.
- Cada número representa el <strong>ID único</strong> de un alumno.


### 3. Crear rango de fechas de Lunes a Viernes

<!-- #region -->
```python
# 2. Generar el rango de fechas de lunes a viernes
fechas = pd.date_range(
    start="2025-02-17",
    end="2025-07-04",
    freq="B"  # 'B' = business days (excluye sábados y domingos)
)
# Formatear como dd/mm/YYYY
fechas_str = fechas.strftime("%d/%m/%Y")
```
<!-- #endregion -->

<strong>Generación de fechas hábiles</strong>

- <code>pd.date_range(...)</code>: Crea todas las fechas entre el <strong>17-feb-2025</strong> y el <strong>4-jul-2025</strong>.

- El parámetro <code>freq="B"</code> filtra únicamente los <strong>días hábiles</strong> (de lunes a viernes).

- <code>.strftime("%d/%m/%Y")</code>: Convierte cada fecha en una cadena con el formato <strong>"día/mes/año"</strong>.


### 4. Construir dataframe vacío

<!-- #region -->
```python
# 3. Crear DataFrame vacío con índices = matrículas y columnas = fechas
df = pd.DataFrame(
    index=matriculas,
    columns=fechas_str
)
```
<!-- #endregion -->

<strong>Creación de la tabla de asistencia</strong>

- Se crea un <code>DataFrame</code> con:
  - Filas indexadas por cada <strong>matrícula</strong>.

  - Columnas correspondientes a cada <strong>fecha del rango</strong>.

- Inicialmente, todas las celdas contienen el valor <code>NaN</code>.


### 5. Rellenar asistencias aleatorias

<!-- #region -->
```python
# 4. Rellenar asistencias de forma aleatoria (“S” o “N”)
np.random.seed(42)  # para reproducibilidad
df[:] = np.random.choice(
    ["S", "N"],
    size=(len(matriculas), len(fechas_str)),
    p = [0.7, 0.3]
)
```
<!-- #endregion -->

<strong>Generación aleatoria de asistencias</strong>

- Se fija la semilla con <code>np.random.seed(42)</code> para garantizar que los resultados sean reproducibles.

- <code>np.random.choice(...)</code>:

  - Elige aleatoriamente entre <strong>"S"</strong> (sí) o <strong>"N"</strong> (no).

  - Tiene 70% de probabilidades de marcar sí.

  - Genera un arreglo del mismo tamaño que el número de alumnos por el número de fechas.

- Ese arreglo se asigna directamente al <strong>DataFrame completo</strong>.


### 6. Convertir el índice en columna

<!-- #region -->
```python
# 5. Preparar para exportar: convertir el índice en columna “MATRICULA”
df.index.name = "MATRICULA"
df.reset_index(inplace=True)
```
<!-- #endregion -->

<strong>Ajuste del índice en el DataFrame</strong>

- Se nombra el índice del DataFrame como <code>"MATRICULA"</code>.

- Luego, con <code>reset_index()</code>:

  - La columna <code>"MATRICULA"</code> pasa al cuerpo del DataFrame.

  - El índice se reemplaza por un índice numérico estándar (<code>0…N</code>).


#### A. Borrar un 1% de asistencias

<!-- #region -->
```python
# A. Borrar un 1% de las asistencias (convertirlas a NaN)
num_filas, num_columnas = df.shape
total_celdas = num_filas * (num_columnas - 1)  # excluye la columna MATRICULA
num_celdas_borrar = int(total_celdas * 0.01)   # 1% del total

if num_celdas_borrar > 0:
    filas_aleatorias = np.random.choice(num_filas, size=num_celdas_borrar, replace=False)
    columnas_aleatorias = np.random.choice(range(1, num_columnas), size=num_celdas_borrar, replace=False)
    
    for i in range(num_celdas_borrar):
        fila = filas_aleatorias[i]
        col = columnas_aleatorias[i]
        df.iat[fila, col] = np.nan

# Convertir todos los NaN a string vacío
df = df.fillna("")
```
<!-- #endregion -->

<strong>Inserción de valores faltantes</strong>

- Se calcula cuántas celdas equivalen al <strong>1%</strong> del total, excluyendo la columna <code>"MATRICULA"</code>.

- Se generan coordenadas aleatorias <strong>sin repetición</strong> para seleccionar combinaciones de filas y columnas.

- Para cada par <code>(fila, columna)</code>, se inserta un valor <code>NaN</code>.

- Al final, todos los <code>NaN</code> se reemplazan por <code>""</code> (cadena vacía) para mantener consistencia.


#### B. Renombrar columnas de fecha

<!-- #region -->
```python
# B. Renombrar columnas de fecha para formato válido (reemplazar / por -)
nuevas_columnas = ['MATRICULA'] + [fecha.replace('/', '-') for fecha in fechas_str]
df.columns = nuevas_columnas
```
<!-- #endregion -->

<strong>Formato de encabezados de fecha</strong>

- Se genera una lista donde cada fecha con formato <code>"dd/mm/YYYY"</code> se transforma a <code>"dd-mm-YYYY"</code>.

- Esa lista se asigna como los nuevos <code>df.columns</code>, manteniendo <strong>"MATRICULA"</strong> como la primera columna.


#### C. Crear carpeta de salida

<!-- #region -->
```python
# C. Crear directorio principal si no existe
os.makedirs("data/asistencia", exist_ok=True)
```
<!-- #endregion -->

<strong>Creación de carpeta de salida</strong>

- Se asegura de que exista la ruta <code>data/asistencia</code> para volcar los archivos generados.


#### D. Exportar en 3 formatos

<!-- #region -->
```python
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
```
<!-- #endregion -->

1. <strong>Barajea</strong>(`.sample(frac=1)`) todo el DataFrame y reinicia índices.

2. Parte el resultado en 3 trozos iguales (o lo más cercanos posible).


#### E. Validación de nombres XML

<!-- #region -->
```python
def make_valid_xml_name(col_name: str) -> str:
    # Si empieza por dígito, anteponemos '_'
    if re.match(r'^[0-9]', col_name):
        return "_" + col_name
    return col_name

# Procesar solo el DataFrame para XML
df_xml = partes[1].copy()

new_cols = []
for c in df_xml.columns:
    if c == "MATRICULA":
        new_cols.append(c)
    else:
        new_cols.append(make_valid_xml_name(c))
df_xml.columns = new_cols
```
<!-- #endregion -->

- Define `make_valid_xml_name()`: si el nombre arranca con número, le antepone _.

- Aplica solo al <strong>trozo 2</strong> (`partes[1]`), porque en XML los tags no pueden empezar con dígito.


#### F. Guardado Final

<!-- #region -->
```python
# 1) CSV
partes[0].to_csv(r"data/asistencia/asistencia.csv", index=False, encoding="utf-8")

# 2) XML
df_xml.to_xml(r"data/asistencia/asistencia.xml", index=False)

# 3) JSON
partes[2].to_json(
    r"data/asistencia/asistencia.json",
    orient="records",
    indent=4
)

print("Proceso completado:")
print(f"- CSV guardado en: data/asistencia/asistencia.csv")
print(f"- XML guardado en: data/asistencia/asistencia.xml")
print(f"- JSON guardado en: data/asistencia/asistencia.json")
```
<!-- #endregion -->

- <strong>Parte 0</strong> → CSV convencional (`.to_csv`).

- <strong>Parte 1</strong> → XML directo de pandas (`.to_xml`), con columnas ya saneadas.

- <strong>Parte 2</strong> → JSON estilo "lista de registros" (`orient='records'`).

- Al final imprime en consola las rutas donde quedan los 3 archivos


### Ejecución


Integramos todo lo anterior dentro del siguiente código y lo corremos:

```python
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
```

Procedemos a cargar la cabecera de los resultados:

```python
pd.read_csv(r"data\asistencia\asistencia.csv").head()
```

```python
pd.read_json(r"data\asistencia\asistencia.json").head()
```

```python
pd.read_xml(r"data\asistencia\asistencia.xml").head()
```

## Dataset de datos demográficos


Finalmente, nos propusimos crear un dataset con algunos datos relevantes del alumnado de esta actividad. Los datos demográficos incluidos son:
1. Nombre

2. Apellido Paterno

3. Apellido Materno

4. Género

5. Fecha de nacimiento

6. Nacionalidad

El detalle es que la fecha de nacimiento debe ser congruente con el semestre de alumno. Para lograr esto, decidimos el año de nacimiento basado en el semestre del alumno, de la siguiente manera:
- 2do semestre = 2009

- 4to semestre = 2008

- 6to semestre = 2007

###### El semestre de los alumnos fue adquirido del archivo <a href = "tmp\calificaciones.csv">calificaciones.csv</a>

También ensuciaremos algunos registros de la siguiente manera:
- Borrar Nombre
- Borrar Género
- Borrar Fecha de nacimiento

Desarrollamos un generador para este último dataset, tomando en cuenta todos estos elementos y a través de los siguientes pasos:


### 1. Importaciones y creación de carpetas

<!-- #region -->
```python
import pandas as pd
import numpy as np
import os
import re
import random

# === Configuración inicial ===
# Crear directorios necesarios
os.makedirs("tmp", exist_ok=True)
os.makedirs("data/datos_demograficos", exist_ok=True)
```
<!-- #endregion -->

1. <strong>Importaciones</strong>
- `pandas` y `numpy` para manejar tablas y arreglos.

- `os` para operaciones de archivos/directorios.

- `re` para expresiones regulares (limpieza de nombres).

- `random` para tomar decisiones aleatorias.

2. <strong>Creación de carpetas</strong>
- `tmp` donde reside el CSV base con matrículas/semestres.

- `data/datos_demograficos` donde se volcarán los nuevos archivos.


### 2. Lectura del CSV base

<!-- #region -->
```python
# === Leer archivo base ===
# Leer el archivo calificaciones.csv para obtener matrículas y semestres
df_base = pd.read_csv(r'tmp/calificaciones.csv', encoding='utf-8-sig')
# Conservar solo las columnas necesarias
df_base = df_base[['MATRICULA', 'SEMESTRE']]
```
<!-- #endregion -->

1. Carga de `tmp/calificaciones.csv` en un DataFrame `df_base`.

2. Filtrado para quedarnos únicamente con las dos columnas que nos interesan:
- `MATRICULA` (ID del alumno)

- `SEMESTRE` (en qué semestre está)


### 3. Definición de listas de datos demográficos

<!-- #region -->
```python
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
```
<!-- #endregion -->

- Tres listas con posibles primeros nombres (femeninos y masculinos).

- Una lista de apellidos comunes.

- Un diccionario de códigos de país a nacionalidades.


### 4. Generación de registros demográficos

<!-- #region -->
```python
# === Generar datos demográficos ===
datos = []

for _, row in df_base.iterrows():
    matricula = row['MATRICULA']
    semestre  = row['SEMESTRE']
    
    # 1) Elegir género y nombre
    genero = random.choice(['F', 'M'])
    if genero == 'F':
        nombre = random.choice(nombres_femeninos)
    else:
        nombre = random.choice(nombres_masculinos)
    
    # 2) Dos apellidos al azar
    apellido_paterno = random.choice(apellidos)
    apellido_materno = random.choice(apellidos)
    
    # 3) Año de nacimiento según semestre
    if semestre == 2:
        año_nacimiento = 2009
    elif semestre == 4:
        año_nacimiento = 2008
    else:  # semestre 6
        año_nacimiento = 2007
    
    # 4) Mes y día aleatorios, ajustando días máximos
    mes_nacimiento = random.randint(1, 12)
    if mes_nacimiento == 2:
        max_dias = 28
    elif mes_nacimiento in [4, 6, 9, 11]:
        max_dias = 30
    else:
        max_dias = 31
    dia_nacimiento = random.randint(1, max_dias)
    fecha_nacimiento = f"{dia_nacimiento:02d}/{mes_nacimiento:02d}/{año_nacimiento}"
    
    # 5) Nacionalidad aleatoria
    nacionalidad = random.choice(list(paises.values()))
    
    # 6) Montar el diccionario de fila
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

# Convertir la lista de dicts en DataFrame
df = pd.DataFrame(datos)
```
<!-- #endregion -->

1. <strong>Iteración</strong> sobre cada alumno del csv base.

2. <strong>Género y nombre</strong>: 50/50 femenino o masculino, sacado de la lista.

3. <strong>Apellidos</strong>: dos apellidos elegidos al azar (padre y madre).

4. <strong>Fecha de nacimiento</strong>:
- Año fijo por semestre (2→2009, 4→2008, 6→2007).
- Mes al azar 1-12, con lógica para saber cuántos días tiene ese mes.
- Día al azar dentro de ese mes.

5. <strong>Nacionalidad</strong>: aleatoria del diccionario `paises`.

6. Cada registro se guarda en la lista `datos` y finalmente se convierte en `df`.


### 5. <i>Ensuciar</i> parcialmente los datos

<!-- #region -->
```python
# === Ensuciar datos ===
campos_ensuciar = ['NOMBRE', 'GENERO', 'FECHA_NACIMIENTO']

# 30% de los registros
num_registros = len(df)
num_ensuciar  = max(1, int(num_registros * 0.30))
registros_ensuciar = np.random.choice(df.index, size=num_ensuciar, replace=False)

for idx in registros_ensuciar:
    # Borrar de 1 a 3 campos al azar
    num_campos_borrar = random.randint(1, 3)
    campos_borrar = random.sample(campos_ensuciar, num_campos_borrar)
    for campo in campos_borrar:
        df.at[idx, campo] = ''
```
<!-- #endregion -->

1. Define los campos candidatos a <i>ensuciar:</i>
- `NOMBRE`
- `GENERO`
- `FECHA_NACIMIENTO`

2. Calcula los registros a ensuciar, máximo el 30% de filas, mínimo 1 registro.

3. Selecciona dicha cantidad de filas al azar.

4. Para cada fila elegida, borra entre 1 y 3 de los campos establecidos (los deja como cadena vacía) para simular datos faltantes.


### 6. Exportación a CSV, JSON y XML

<!-- #region -->
```python
# === Exportar a múltiples formatos ===

# Función para limpiar nombres XML
def sanitize_xml_name(name):
    sanitized = re.sub(r'[^\w]', '_', name)     # espacios/acentos → _
    if re.match(r'^\d', sanitized):             # si empieza con dígito...
        sanitized = 'col_' + sanitized          # ...antepone 'col_'
    return sanitized

# 1) CSV
df.to_csv(
    r'data/datos_demograficos/datos_demograficos.csv',
    index=False,
    encoding='utf-8-sig'
)

# 2) JSON
df.to_json(
    r'data/datos_demograficos/datos_demograficos.json',
    orient='records',
    indent=4,
    force_ascii=False
)

# 3) XML
nuevos_nombres = {col: sanitize_xml_name(col) for col in df.columns}
df_xml = df.rename(columns=nuevos_nombres)

xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<datos_demograficos>\n'
for _, row in df_xml.iterrows():
    xml_content += '  <registro>\n'
    for col_name, value in row.items():
        # Escapar &, <, >
        if isinstance(value, str):
            value = (value.replace('&', '&amp;')
                          .replace('<', '&lt;')
                          .replace('>', '&gt;'))
        xml_content += f'    <{col_name}>{value}</{col_name}>\n'
    xml_content += '  </registro>\n'
xml_content += '</datos_demograficos>'

with open(
    r'data/datos_demograficos/datos_demograficos.xml',
    'w',
    encoding='utf-8'
) as xml_file:
    xml_file.write(xml_content)

print("Proceso completado exitosamente!")
print("Archivos generados en 'data/datos_demograficos':")
print("- datos_demograficos.csv")
print("- datos_demograficos.json")
print("- datos_demograficos.xml")
```
<!-- #endregion -->

1. `sanitize_xml_name()`: convierte nombres de columna a etiquetas válidas para XML (sin espacios ni que empiecen en número).

2. <strong>CSV</strong>: exportado todo `df` a `datos_demograficos.csv` con BOM.

3. <strong>JSON</strong>: estilo lista de registros, con indentación y soportando tildes.

4. <strong>XML</strong>:
- Renombra columnas en `df_xml` usando la función de sanidad

- Escapa caracteres especiales en los valores.
- Graba el resultado en `datos_demograficos.xml`

5. <strong>Mensajes finales</strong> en consola con las rutas generadas


### 7. Ejecución


Integramos todo lo anterior en la siguiente celda:

```python
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
```

y cargamos la cabecera de los resultados:

```python
pd.read_csv(r"data\datos_demograficos\datos_demograficos.csv").head()
```

```python
pd.read_json(r"data\datos_demograficos\datos_demograficos.json").head()
```

```python
pd.read_xml(r"data\datos_demograficos\datos_demograficos.xml").head()
```

# Unión y cálculo de métricas


Para nuestra actividad, decidimos implementar una fase en la que se juntan todos los datos a través de un identificador en común (`MATRICULA`) y luego decidimos calcular las siguientes métricas para su posterior análisis:
1. Promedio de alumno.

2. Total de asistencias.

3. Total de inasistencias.

4. Porcentaje de asistencias.

5. Casilla de riesgo de reprobación (`1` o `0` dependiendo de la asistencia `<70%` y promedio `<6`).

6. Promedio por materia (tomando en cuenta que hay alumnos que no toman algunas materias dado su semestre).

Asimismo, los dataset recibidos tienen algunos registros sucios, que limpiaremos aplicando las siguientes reglas de corrección:
1. Asistencias: Marcar vacíos como N

2. Calificaciones: Usar promedio para sobreescribir calificaciones anormales (100 veces más grande/chica de lo normal).

3. Datos demográficos: 
    - Agregar alumno/a dependiendo el género.

    - Rellenar géneros vacíos tomando en cuenta el nombre


Esta fase se puede dividir dentro de las siguientes secciones:


## 1. Importaciones y Configuración Inicial

<!-- #region -->
```python
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
```
<!-- #endregion -->

- Importa librerías clave para manejar datos, archivos, expresiones regulares y fechas.

- Define `PATHS`, donde buscar cada tipo de dato.

- Declara listas de nombres femeninos/masculinos para la inferencia de género.

- Mapea semestres (`2`, `4`, `6`) a sus asignaturas válidas.


## 2. Funciones de Carga de Archivos

<!-- #region -->
```python
def cargar_csv(ruta):
    return pd.read_csv(ruta, encoding='utf-8-sig')

def cargar_json(ruta):
    return pd.read_json(ruta, encoding='utf-8')

def cargar_xml(ruta):
    try:
        return pd.read_xml(ruta)
    except:
        # parseo manual con regex si falla
        with open(ruta, 'r', encoding='utf-8') as f:
            xml_content = f.read()
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
    for formato in ['csv','json','xml']:
        ruta = os.path.join(PATHS[tipo], f"{tipo}.{formato}")
        if os.path.exists(ruta):
            if formato == 'csv':
                df_temp = cargar_csv(ruta)
            elif formato == 'json':
                df_temp = cargar_json(ruta)
            else:
                df_temp = cargar_xml(ruta)
                # renombrados y ajustes específicos para XML…
            df_temp = df_temp.fillna('')
            dfs.append(df_temp)
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        df = df.drop_duplicates().dropna(how='all')
        return df
    return pd.DataFrame()
```
<!-- #endregion -->

- Proporciona funciones para leer CSV, JSON y XML.

- `cargar_dataset` busca en la carpeta correspondiente, carga todos los formatos existentes, unifica en un solo `DataFrame` y limpia duplicados y filas vacías.


## 3. Utilidades de Inferencia y Formateo

<!-- #region -->
```python
def inferir_genero(nombre):
    nombre = str(nombre).strip()
    if nombre in NOMBRES_FEMENINOS: return 'F'
    elif nombre in NOMBRES_MASCULINOS: return 'M'
    return ''

def formatear_fecha(fecha_str):
    if not fecha_str or fecha_str in ['None','nan','']: return None
    fecha_limpia = re.sub(r'[^0-9/]','', str(fecha_str))
    formatos = ['%d/%m/%Y','%Y/%m/%d','%m/%d/%Y','%d%m%Y','%Y%m%d']
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_limpia, fmt).strftime('%d/%m/%Y')
        except ValueError:
            continue
    return fecha_limpia
```
<!-- #endregion -->

- `inferir_genero`: marca `'F'` o `'M'` según el nombre esté en las listas, o devuelve una cadena vacía.

- `formatear_fecha`: limpia la cadena, prueba varios patrones de parseo y devuelve la fecha en formato `dd/mm/YYYY`, o la cadena limpia si no encaja.


## 4. Corrección de Asistencias y Calificaciones

<!-- #region -->
```python
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
```
<!-- #endregion -->

- **Asistencias**:
  - Convierte marcadores “S/N” y variantes a booleanos `True`/`False`.

- **Calificaciones**:
  - Normaliza la columna `SEMESTRE`.
  
  - Convierte notas a valores numéricos.
  - Elimina notas de materias que no correspondan al semestre.
  - Calcula el promedio de cada alumno (`70` si no hay notas).
  - Corrige valores anómalos (menores a `1` o mayores a `100`).
  - Añade la columna `PROMEDIO`.


## 5. Corrección de Datos Demográficos

<!-- #region -->
```python
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
```
<!-- #endregion -->

- Agrega el semestre al `DataFrame` demográfico.

- Completa nombres vacíos con “Alumno(a)”.
- Infiera o rellena el género faltante.
- Rellena fechas de nacimiento vacías con fechas por defecto según el semestre y las formatea.
- Limpia columnas sobrantes y deja solo las finales, renombradas.


## 6. Función Principal y Consolidación

<!-- #region -->
```python
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
```
<!-- #endregion -->

- Carga y corrige los tres datasets principales.

- Los fusiona para crear un único `DataFrame`.
- Calcula totales, porcentajes y un flag de riesgo.
- Añade una fila con los promedios por materia.
- Exporta el resultado a un archivo CSV y reporta el resumen por consola.


## 7. Ejecución y comprobación


### Ejecución


Todo lo anterior lo integramos dentro de la siguiente celda y procedemos a correrla:

```python
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
```

Procedemos a cargar una muestra del resultado:

```python
pd.read_csv(r"data\consolidado\datos_consolidados.csv").head()
```

### Comprobación


Corroboramos que:


#### 1. Hay 100 registros de alumnos + la fila de promedio por materia


<img src = "media\comprob\1. 100 registros.png">


<strong>¡Podemos confirmar que todo esta en orden!</strong>


#### 2. Los alumnos tienen las materias correctas


Comprobamos que los alumnos de <strong>segundo</strong> tienen las materias que les corresponden:


<img src = "media\comprob\2.1 Segundo.png">


Comprobamos que los alumnos de <strong>cuarto</strong> tienen las materias que les corresponden:


<img src = "media\comprob\2.3 Cuarto.png">


Comprobamos que los alumnos de <strong>sexto</strong> tienen las materias que les corresponden:


<img src = "media\comprob\2.2 Sexto.png">


<strong>¡Podemos confirmar que todo esta en orden!</strong>


#### 3. El promedio fue bien calculado para los alumnos de cada semestre


Usamos las calificaciones de un alumno de cada semestre:


<img src = "media\comprob\3.1 Promedios.png">


y las contrastamos con las originales:


<img src = "media\comprob\3.2 Promedios.png">


En este caso, los promedios son de alumnos de:
1. <strong>Segundo Semestre</strong>
2. <strong>Sexto Semestre</strong>
3. <strong>Cuarto Semestre</strong>


#### 4. El conteo de asistencias es correcto


Realizamos las siguientes operaciones dentro de una hoja de cálculo:


<img src = "media\comprob\4. Asistencias.png">


donde se implementaron las fórmulas:
1. <strong>Total de días</strong>: `=COLUMNAS(A2:CV2)`

2. <strong>Asistencias</strong>: `=SUMAR.SI(A2:CV2, 1)`

3. <strong>Inasistencias</strong>: `=CONTAR.SI(A2:CV2, 0)`

Y tomando en cuenta que hubo un rango de 100 días, <strong>el porcentaje de asistencias es del 69%</strong>.

Contrastamos estos datos con los resultados del proceso previo: 


<img src = "media\comprob\4.2 Asistencias.png">


<strong>¡Podemos confirmar que todo esta en orden!</strong>


#### 5. El promedio de una materia esta siendo calculado correctamente a pesar de los NaN


<img src = "media\comprob\5.1 Promedio.png">


Donde se implementó la fórmula `PROMEDIO` de Excel, que ignora registros vacíos.

Luego, contrastamos con el cálculo del proceso de extracción:


<img src = "media\comprob\5.2 Promedio.png">


<strong>¡Podemos confirmar que todo esta en orden!</strong>


###### El archivo con las hojas de la comprobación se encuentra en <a href = "tmp\Comprobacion.xlsx"><i>Comprobacion.xlsx</i></a>


# Estructura Multidimensional


## Propuesta


Usando los datos del csv consolidado, realizamos el siguiente diccionario de datos:

```python
pd.read_excel(r"tmp\Diccionario - Consolidado.xlsx")
```

###### Para mejor visualización consulte <a href = "tmp\Diccionario - Consolidado.xlsx"><i>Diccionario - Consolidado.xlsx</i></a>


Y usamos esta información para desarrollar el siguiente diseño de una base que nos permitirá realizar análisis multidimensional:


<img src = "media\diagramas\1. Cubo.svg">


###### Para mejor visualización consulte <a href = "media\diagramas\1. Cubo.svg"><i>1. Cubo.svg</i></a>


## Implementación


Para lograr migrar nuestros datos de csv a una estructura multidimensional en una base de datos relacional, hicimos uso de un código desarollado en las siguientes etapas:


### 1. Importación de librerías y definición de materias

<!-- #region -->
```python
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
```
<!-- #endregion -->

Importa las librerías **Pandas** y **NumPy**, y define un diccionario que contiene las materias organizadas por semestre (**2**, **4** y **6**). Cada semestre tiene una lista de nombres de materias específicas.


### 2. Preparación de datos iniciales

<!-- #region -->
```python
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
```
<!-- #endregion -->

- Combina todas las materias de todos los semestres en una sola lista (`todas_materias`).
- Carga el archivo CSV consolidado en un **DataFrame**.
- Define las columnas demográficas relevantes.
- Separa los datos en dos **DataFrames**: uno para promedios de materias y otro para datos de alumnos.


### 3. Construcción de dimensión MATERIA


<!-- #region -->
```python
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
```
<!-- #endregion -->

**Crea la dimensión DIM_MATERIA con:**

- **nombre_materia**: Nombre de cada materia.  
- **PROMEDIO_MATERIA**: Promedio general de cada materia.  
- **materia_id**: ID único generado secuencialmente.  

Finalmente, redondea los promedios a 2 decimales.


### 4. Construcción de dimensión ASISTENCIAS

<!-- #region -->
```python
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
```
<!-- #endregion -->

**Construye la dimensión DIM_ASISTENCIAS** con:

- Datos de asistencia por **matrícula** y **semestre**  
- Conversión de asistencias/inasistencias a **enteros**  
- Redondeo del **porcentaje de asistencia** a 2 decimales  
- Eliminación de **registros duplicados**


### 5. Construcción de tabla de hechos


<!-- #region -->
```python
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
```
<!-- #endregion -->

- Transforma los datos a **formato largo** (una fila por estudiante-materia)  
- Redondea **promedios** y **porcentajes** a 2 decimales  
- Mapea nombres de materias a **IDs** usando un diccionario  
- Elimina la columna **redundante** de nombre de materia


### 6. Transformación de tipos de datos


<!-- #region -->
```python
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
```
<!-- #endregion -->

- Convierte **fechas de nacimiento** al formato estándar ISO (YYYY-MM-DD)  
- Transforma el **riesgo de reprobación** a entero (boolean)  
- Reemplaza valores **NaN** en porcentajes por **None** para mejor manejo en SQL  
- Maneja errores en conversión de fechas con el modo **coerce**


### 7. Generación de script SQL


<!-- #region -->
```python
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
```
<!-- #endregion -->

- Crea 3 tablas: **DIM_MATERIA**, **DIM_ASISTENCIAS** y **HECHOS_DEMOGRAFICOS**  
- Define relaciones mediante **claves foráneas**  
- Inserta datos en bloques de **1000 registros** para optimización  
- Maneja **valores nulos** y escapa **caracteres especiales**  
- Convierte **tipos de datos** adecuadamente para SQL  
- Deshabilita temporalmente las **restricciones de claves foráneas** durante la carga  
- Genera un archivo **cubo_escolar.sql** con todo el esquema y datos


### 8. Ejecución del código


Todo lo anterior lo integramos dentro de la siguiente celda y la corremos:

```python
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
```

y comprobamos que el archivo se haya creado exitosamente:


<img src = "media\7. Comprobamos.jpg">


# Creación de dashboard web interactivo


Con tal de visualizar datos de una forma entendible, nos propusimos crear un dashboard web que cumpla los siguientes criterios:
1. Cuenta con una gráfica de barras
2. Cuenta con una gráfica de dispersión
3. Su interfaz nos permite aplicar filtros a los datos graficados

La estructura propuesta del código del dashboard fue:
```
/
├── flask_app.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       └── dashboard.png
└── templates/
    └── dashboard.html
```

permitiendonos separar cada tipo de código (comunicación con la base de datos, estilos, estructura de la página, etc.) en un archivo por separado.

Esta fase se dividió en las siguientes etapas:


## Creación de `flask_app.py`


Para la creación del `flask_app.py` seguimos los siguientes pasos:


### 1. Importaciones y Configuración Inicial


<!-- #region -->
```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, bindparam
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool, ColumnDataSource, Range1d, Legend, LegendItem, Span
from bokeh.palettes import Category10
import pandas as pd
import numpy as np
from collections import defaultdict
import math

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://'
    'fedivej259:24062025_@'
    'fedivej259.mysql.pythonanywhere-services.com/'
    'fedivej259$cubo'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```
<!-- #endregion -->

Importa todas las bibliotecas necesarias y configura la aplicación Flask con la conexión a una base de datos MySQL alojada en PythonAnywhere. Se inicializa SQLAlchemy para la gestión de la base de datos y se definen recursos clave para visualización con Bokeh.


### 2. Ruta Principal del Dashboard

<!-- #region -->
```python
@app.route('/')
def dashboard():
    try:
        # Obtener parámetros de filtro
        semestres_filtro = request.args.getlist('semestre')
        generos_filtro = request.args.getlist('genero')
        materias_filtro = request.args.getlist('materia_id')

        # Obtener datos para los filtros
        semestres = obtener_semestres()
        generos = obtener_generos()
        materias_agrupadas = obtener_materias_agrupadas()

        # Construir condiciones WHERE dinámicas
        condiciones = []
        parametros = {}
        bind_params = []
        
        if semestres_filtro and 'Todos' not in semestres_filtro:
            condiciones.append("H.SEMESTRE IN :semestres")
            parametros['semestres'] = tuple(semestres_filtro)
            bind_params.append(bindparam('semestres', expanding=True))
            
        if generos_filtro and 'Todos' not in generos_filtro:
            condiciones.append("H.GENERO IN :generos")
            parametros['generos'] = tuple(generos_filtro)
            bind_params.append(bindparam('generos', expanding=True))
            
        if materias_filtro and '0' not in materias_filtro:
            condiciones.append("H.materia_id IN :materias")
            parametros['materias'] = tuple(map(int, materias_filtro))
            bind_params.append(bindparam('materias', expanding=True))
            
        # Agregar condición fija para PORCENTAJE no nulo
        condiciones.append("H.PORCENTAJE IS NOT NULL")
        
        where_clause = "WHERE " + " AND ".join(condiciones) if condiciones else ""
```
<!-- #endregion -->

Define la ruta principal `/` que gestiona el dashboard. Recibe parámetros de filtro (`semestre`, `género`, `materia`) desde la URL, obtiene datos para los controles de filtrado y construye dinámicamente cláusulas SQL `WHERE` usando `bindparam` para prevenir inyecciones SQL. Siempre incluye la condición de porcentaje no nulo.


### 3. Consulta para Gráfico de Barras


<!-- #region -->
```python
        # 1. Gráfico de barras: Promedio por materia, semestre y género
        query_text = f"""
            SELECT 
                H.SEMESTRE,
                M.materia_id,
                M.nombre_materia,
                H.GENERO,
                AVG(H.PORCENTAJE) AS promedio
            FROM HECHOS_DEMOGRAFICOS H
            JOIN DIM_MATERIA M ON H.materia_id = M.materia_id
            {where_clause}
            GROUP BY H.SEMESTRE, M.materia_id, M.nombre_materia, H.GENERO
            ORDER BY H.SEMESTRE, M.nombre_materia, H.GENERO
        """
        
        # Crear objeto text con bindparams para expansión
        query1 = text(query_text)
        if bind_params:
            query1 = query1.bindparams(*bind_params)
        
        result1 = db.session.execute(query1, parametros)
        df_barras = pd.DataFrame(result1, columns=['semestre', 'materia_id', 'materia', 'genero', 'promedio'])
```
<!-- #endregion -->

Ejecuta una consulta SQL que calcula el promedio de porcentaje agrupado por semestre, materia y género. Los resultados se almacenan en un DataFrame de Pandas para su procesamiento posterior. Utiliza parámetros enlazados para seguridad y manejo de listas variables.


### 4. Construcción del Gráfico de Barras

<!-- #region -->
```python
        if not df_barras.empty:
            # ... (procesamiento de datos y mapeo de colores)
            
            source_barras = ColumnDataSource(data)
            
            # Crear figura con barras HORIZONTALES
            p1 = figure(
                y_range=data['materia_genero'],
                x_range=Range1d(0, 120),
                title="Promedio por Materia y Género",
                height=800,
                width=1000,
                tools=herramientas_barras,
                toolbar_location="above",
                y_axis_label="Materia y Género",
                x_axis_label="Promedio (%)"
            )
            
            # ... (configuración de ejes, hover y leyenda)
            
            # Añadir separadores de semestre y etiquetas
            for i, (semestre, position) in enumerate(semestre_positions.items()):
                # ... (cálculo de posiciones)
                if i < len(semestre_positions) - 1:
                    separator = Span(...)
                    p1.add_layout(separator)
                
                p1.text(
                    x=105,
                    y=center_pos,
                    text=[f"S{semestre}"],
                    # ... (estilo de texto)
                )
        else:
            # Crear figura vacía si no hay datos
            p1 = figure(...)
```
<!-- #endregion -->

Genera un gráfico de barras horizontales interactivo con Bokeh. Organiza las barras por materia y género, agrupadas por semestre. Incluye separadores visuales entre semestres, etiquetas de semestre y una leyenda interactiva que permite mutear géneros. Maneja casos sin datos mostrando un mensaje.




### 5. Consulta para Gráfico de Dispersión


<!-- #region -->
```python
        # 2. Gráfico de dispersión: Promedio vs Asistencia
        query_text2 = f"""
            SELECT H.PORCENTAJE AS promedio, A.PORCENTAJE_ASISTENCIA, 
                   M.nombre_materia, H.SEMESTRE, H.GENERO
            FROM HECHOS_DEMOGRAFICOS H
            JOIN DIM_ASISTENCIAS A
              ON H.MATRICULA = A.MATRICULA
             AND H.SEMESTRE = A.SEMESTRE
            JOIN DIM_MATERIA M ON H.materia_id = M.materia_id
            {where_clause}
        """
        
        query2 = text(query_text2)
        if bind_params:
            query2 = query2.bindparams(*bind_params)
        
        result2 = db.session.execute(query2, parametros)
        df_disp = pd.DataFrame(result2, columns=['promedio', 'asistencia', 'materia', 'semestre', 'genero'])
```
<!-- #endregion -->

Realiza una segunda consulta para obtener datos de promedio versus asistencia. Une tablas de hechos demográficos, asistencias y materias usando la misma cláusula `WHERE` dinámica generada previamente.


### 6. Construcción del Gráfico de Dispersión


<!-- #region -->
```python
        if not df_disp.empty:
            # ... (preparación de datos y colores)
            
            p2 = figure(
                title="Promedio vs Asistencia",
                height=500,
                width=800,
                tools=herramientas_disp,
                toolbar_location="above"
            )
            
            scatter = p2.scatter(
                'promedio',
                'asistencia',
                size=10,
                alpha=0.6,
                color='color',
                source=source_disp,
                legend_field='genero'
            )
            
            # ... (configuración de ejes, hover y leyenda interactiva)
        else:
            # Mostrar mensaje cuando no hay datos
            p2 = figure(...)
```
<!-- #endregion -->

Crea un gráfico de dispersión que relaciona el promedio académico con el porcentaje de asistencia. Los puntos se colorean según el género e incluyen tooltips detallados. La leyenda permite mutear categorías de género interactivamente.


### 7. Renderización de Resultados


<!-- #region -->
```python
        # Generar componentes Bokeh
        script1, div1 = components(p1)
        script2, div2 = components(p2)
        
        # Obtener recursos CDN
        bokeh_resources = {
            'js': CDN.js_files,
            'css': CDN.css_files
        }

        return render_template(
            'dashboard.html',
            script1=script1, 
            div1=div1,
            script2=script2, 
            div2=div2,
            bokeh_resources=bokeh_resources,
            semestres=semestres,
            generos=generos,
            materias_agrupadas=materias_agrupadas,
            filtro_semestre=semestres_filtro,
            filtro_genero=generos_filtro,
            filtro_materia=materias_filtro
        )
```
<!-- #endregion -->

Convierte los gráficos Bokeh en componentes HTML/JS y prepara los recursos necesarios (CDN). Renderiza la plantilla `dashboard.html` pasando los gráficos, recursos CDN, datos para los filtros y valores actuales seleccionados.


### 8. Funciones Auxiliares


<!-- #region -->
```python
def obtener_semestres():
    """Obtener lista de semestres disponibles"""
    query = text("SELECT DISTINCT SEMESTRE FROM HECHOS_DEMOGRAFICOS ORDER BY SEMESTRE DESC")
    result = db.session.execute(query)
    return ['Todos'] + [str(row[0]) for row in result]

def obtener_generos():
    """Obtener lista de géneros disponibles"""
    query = text("SELECT DISTINCT GENERO FROM HECHOS_DEMOGRAFICOS")
    result = db.session.execute(query)
    return ['Todos'] + [row[0] for row in result]

def obtener_materias_agrupadas():
    """Obtener lista de materias disponibles agrupadas por semestre"""
    query = text("""
        SELECT 
            H.SEMESTRE,
            M.materia_id,
            M.nombre_materia
        FROM HECHOS_DEMOGRAFICOS H
        JOIN DIM_MATERIA M ON H.materia_id = M.materia_id
        WHERE H.PORCENTAJE IS NOT NULL
        GROUP BY H.SEMESTRE, M.materia_id, M.nombre_materia
        ORDER BY H.SEMESTRE DESC, M.nombre_materia
    """)
    result = db.session.execute(query)
    
    # ... (agrupamiento por semestre)
    return materias_agrupadas
```
<!-- #endregion -->

Funciones que obtienen datos para los controles de filtrado: semestres (incluyendo opción "Todos"), géneros disponibles, y materias organizadas por semestre. Las materias se agrupan en una estructura de diccionario por semestre.




### 9. Manejo de Errores y Ejecución


<!-- #region -->
```python
    except Exception as e:
        # Capturar cualquier error y mostrar detalles
        import traceback
        error_message = f"Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_message)
        return f"""
        <h1>Error en la aplicación</h1>
        <pre>{error_message}</pre>
        <p>Verifica:</p>
        <ul>
            <li>El nombre de la BD: 'fedivej259$cubo'</li>
            <li>Usuario: 'fedivej259'</li>
            <li>Host: 'fedivej259.mysql.pythonanywhere-services.com'</li>
            <li>Contraseña: '24062025_' (con guión bajo final)</li>
            <li>Que el usuario tenga permisos en PythonAnywhere</li>
        </ul>
        """

if __name__ == '__main__':
    app.run(debug=True)
```
<!-- #endregion -->

Captura excepciones mostrando detalles técnicos y sugerencias para resolver errores de conexión a la base de datos. Inicia el servidor Flask en modo debug cuando se ejecuta directamente.



###### Para mejor visualización consulte <a href = "anexo\flask_app.py"><i>flask_app.py</i></a>


## Creación del `dashboard.html`


Para la creación del `dashboard.html` seguimos los siguientes pasos:


### 1. Estructura Básica del Documento HTML

<!-- #region -->
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Académico</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    
      <link rel="icon" 
        type="image/png" 
        href="{{ url_for('static', filename='img/dashboard.png') }}">
    
    <!-- Incluir recursos de Bokeh -->
    {% for css in bokeh_resources['css'] %}
        <link rel="stylesheet" href="{{ css }}">
    {% endfor %}
    {% for js in bokeh_resources['js'] %}
        <script src="{{ js }}"></script>
    {% endfor %}
</head>
<body>
```
<!-- #endregion -->

Define la estructura básica del documento HTML con metadatos esenciales. Incluye enlaces a recursos CSS locales y recursos CDN de Bokeh cargados dinámicamente. Configura un favicon personalizado para la aplicación.




### 2. Selector de Tema y Encabezado


<!-- #region -->
```html
    <div class="theme-switcher">
        <button class="theme-btn" id="theme-toggle">Modo Oscuro</button>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>Dashboard Académico</h1>
        </div>
```
<!-- #endregion -->

Muestra un botón para alternar entre modo oscuro y claro en la esquina superior derecha. Incluye un encabezado principal con el título "Dashboard Académico" dentro de un contenedor principal.



### 3. Tarjeta de Instrucciones


<!-- #region -->
```html
        <div class="instruction-card">
            <h3>¿Cómo usar este dashboard?</h3>
            <ul>
                <li><strong>Filtros:</strong> Seleccione semestres, géneros y materias para filtrar los datos.</li>
                <li><strong>Gráfico de Barras:</strong> Muestra el promedio por materia y género. Haga clic en la leyenda para resaltar/ocultar géneros.</li>
                <li><strong>Gráfico de Dispersión:</strong> Relación entre promedio y asistencia. Puede hacer zoom y pan para explorar.</li>
                <li><strong>Reiniciar Filtros:</strong> Use el botón rojo para volver a la vista inicial.</li>
                <li><strong>Modo Oscuro:</strong> Active/desactive con el botón superior derecho.</li>
            </ul>
        </div>
```
<!-- #endregion -->

Proporciona una guía de usuario con instrucciones claras sobre cómo interactuar con el dashboard. Utiliza una lista con elementos destacados en negrita para explicar las funcionalidades clave.




### 4. Formulario de Filtros


<!-- #region -->
```html
        <form method="GET" class="filtros">
            <div class="filtro-group">
                <h3>Filtros:</h3>
            </div>
            
            <div class="filtro-row">
                <div class="filtro-col">
                    <label for="semestre">Semestre:</label>
                    <select name="semestre" multiple size="5">
                        {% for semestre in semestres %}
                            <option value="{{ semestre }}" 
                                {% if semestre in filtro_semestre %}selected{% endif %}>
                                {{ semestre }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filtro-col">
                    <label for="genero">Género:</label>
                    <select name="genero" multiple size="5">
                        {% for genero in generos %}
                            <option value="{{ genero }}" 
                                {% if genero in filtro_genero %}selected{% endif %}>
                                {{ genero }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filtro-col">
                    <label for="materia_id">Materia:</label>
                    <select name="materia_id" multiple size="10">
                        <option value="0" {% if '0' in filtro_materia %}selected{% endif %}>Todas las materias</option>
                        {% for semestre, materias in materias_agrupadas %}
                            <optgroup label="Semestre {{ semestre }}">
                                {% for id, nombre in materias %}
                                    <option value="{{ id }}" 
                                        {% if id|string in filtro_materia %}selected{% endif %}>
                                        {{ nombre }}
                                    </option>
                                {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
            </div>
```
<!-- #endregion -->

Crea un formulario con tres filtros de selección múltiple:

1. Semestre: Lista de semestres disponibles con selección persistente

2. Género: Opciones de género con selección persistente

3. Materia: Lista jerárquica agrupada por semestre con opción "Todas las materias"


### 5. Botones de Acción


<!-- #region -->
```html
            <div class="button-group">
                <button type="submit">Aplicar Filtros</button>
                <button type="button" class="reset-btn" id="reset-btn">Reiniciar Filtros</button>
            </div>
        </form>
```
<!-- #endregion -->

Añade dos botones de acción:

- Aplicar Filtros: Envía el formulario para actualizar los gráficos

- Reiniciar Filtros: Botón rojo para limpiar todas las selecciones


### 6. Contenedores para Gráficos Bokeh

<!-- #region -->
```html
        <div class="grafico">
            <h2>Promedio por Materia y Género</h2>
            <div class="bokeh-wrapper">
                {{ div1 | safe }}
            </div>
            {{ script1 | safe }}
        </div>
        
        <div class="grafico">
            <h2>Promedio vs Asistencia</h2>
            <div class="bokeh-wrapper">
                {{ div2 | safe }}
            </div>
            {{ script2 | safe }}
        </div>
    </div>
```
<!-- #endregion -->

Incrusta los componentes de Bokeh generados por Flask:

1. Primer gráfico: Promedio por materia y género con su contenedor

2. Segundo gráfico: Dispersión de promedio vs asistencia con su contenedor

3. Usa `| safe` para renderizar correctamente el HTML generado


### 7. Scripts Finales y Cierre


<!-- #region -->
```html
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```
<!-- #endregion -->

Incluye el archivo JavaScript local para funcionalidades interactivas y cierra las etiquetas del documento HTML.


###### Para mejor visualización consulte <a href = "anexo\dashboard.html"><i>dashboard.html</i></a>


## Creación de `styles.css`


Para la creación del `styles.css` seguimos los siguientes pasos:


### 1. Variables CSS Globales y Estilos Base


```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2980b9;
    --background-light: #f5f7fa;
    --background-dark: #1a1a2e;
    --card-light: #ffffff;
    --card-dark: #16213e;
    --text-light: #333333;
    --text-dark: #e6e6e6;
    --border-light: #e0e0e0;
    --border-dark: #30475e;
    --instruction-card: #e1f0fa;
    --instruction-card-dark: #1e3a5f;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: var(--background-light);
    color: var(--text-light);
    transition: background-color 0.3s, color 0.3s;
}

body.dark-mode {
    background-color: var(--background-dark);
    color: var(--text-dark);
}
```


Define variables CSS para colores clave que permiten alternar entre modos claro/oscuro. Configura estilos base para el cuerpo del documento con transiciones suaves para cambios de tema.



### 2. Contenedor Principal y Encabezado



```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    background-color: var(--card-light);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    transition: background-color 0.3s;
}

body.dark-mode .container {
    background-color: var(--card-dark);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--primary-color);
}

.header h1 {
    color: var(--primary-color);
    font-size: 2.5rem;
    margin: 0;
    padding: 10px 0;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
```


Diseña el contenedor principal con dimensiones máximas, sombras y bordes redondeados. El encabezado incluye un borde inferior decorativo con el color primario y un título con efecto de sombra de texto.


### 3. Selector de Tema e Instrucciones



```css
.theme-switcher {
    position: absolute;
    top: 25px;
    right: 20px;
}

.theme-btn {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 30px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.theme-btn:hover {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
}

.instruction-card {
    background-color: var(--instruction-card);
    border-left: 5px solid var(--primary-color);
    padding: 15px 20px;
    border-radius: 5px;
    margin-bottom: 25px;
    transition: background-color 0.3s;
}

body.dark-mode .instruction-card {
    background-color: var(--instruction-card-dark);
    border-left: 5px solid var(--secondary-color);
}

.instruction-card h3 {
    margin-top: 0;
    color: var(--primary-color);
}

body.dark-mode .instruction-card h3 {
    color: #64b5f6;
}

.instruction-card ul {
    padding-left: 20px;
}
```


Posiciona el botón de cambio de tema en la esquina superior derecha con efectos hover. La tarjeta de instrucciones muestra un borde lateral de acento y cambia completamente de apariencia en modo oscuro.




### 4. Sistema de Filtros



```css
.filtros {
    background-color: rgba(240, 240, 240, 0.7);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 25px;
    transition: background-color 0.3s;
    border: 1px solid var(--border-light);
}

body.dark-mode .filtros {
    background-color: rgba(30, 30, 46, 0.7);
    border-color: var(--border-dark);
}

.filtros label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: var(--primary-color);
}

body.dark-mode .filtros label {
    color: #64b5f6;
}

.filtros select {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid var(--border-light);
    border-radius: 5px;
    background-color: white;
    color: var(--text-light);
    transition: all 0.3s;
    font-size: 14px;
}

body.dark-mode .filtros select {
    background-color: #2c3e50;
    border-color: var(--border-dark);
    color: var(--text-dark);
}

.filtros button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
    margin-right: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.filtros button:hover {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
}

.reset-btn {
    background-color: #e74c3c !important;
}

.reset-btn:hover {
    background-color: #c0392b !important;
}
```


Crea un área de filtros semitransparente con controles de selección múltiple. Los botones tienen efectos interactivos y el botón de reinicio se destaca en rojo. Todos los elementos se adaptan visualmente al modo oscuro.




### 5. Contenedores de Gráficos



```css
.grafico {
    margin-bottom: 40px;
    border: 1px solid var(--border-light);
    border-radius: 8px;
    padding: 20px;
    background-color: var(--card-light);
    transition: all 0.3s;
}

body.dark-mode .grafico {
    background-color: var(--card-dark);
    border-color: var(--border-dark);
}

.grafico h2 {
    margin-top: 0;
    color: var(--primary-color);
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-light);
    font-size: 1.8rem;
}

body.dark-mode .grafico h2 {
    color: #64b5f6;
    border-bottom-color: var(--border-dark);
}

.bokeh-wrapper {
    overflow: auto;
    border: 1px solid var(--border-light);
    padding: 15px;
    border-radius: 5px;
    margin-top: 15px;
    background-color: white;
    transition: all 0.3s;
}

body.dark-mode .bokeh-wrapper {
    background-color: #2c3e50;
    border-color: var(--border-dark);
}
```


Diseña contenedores para gráficos con bordes, relleno y fondo adaptativos. Los títulos de sección incluyen bordes inferiores decorativos. El contenedor Bokeh tiene desplazamiento para gráficos grandes y cambia de fondo en modo oscuro.




### 6. Componentes Adicionales y Utilidades



```css
.filtro-group {
    margin-bottom: 20px;
}

.filtro-group h3 {
    margin-bottom: 12px;
    font-size: 18px;
    color: var(--text-light);
}

body.dark-mode .filtro-group h3 {
    color: var(--text-dark);
}

optgroup {
    font-weight: bold;
    font-style: normal;
    background-color: #f9f9f9;
}

body.dark-mode optgroup {
    background-color: #2c3e50;
}

optgroup option {
    padding-left: 20px;
    font-weight: normal;
}

.filtro-row {
    display: flex;
    flex-wrap: wrap;
    gap: 25px;
}

.filtro-col {
    flex: 1;
    min-width: 250px;
}

.bokeh-plot {
    overflow-x: auto;
}

.bokeh-wrapper .bk-root .bk-axis-label {
    font-size: 12pt;
}

.button-group {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}
```


Organiza los filtros en columnas flexibles responsivas. Personaliza grupos de opciones en selects con sangrías y fondos diferenciados. Ajusta el tamaño de fuente de etiquetas en gráficos Bokeh y agrupa botones con espaciado uniforme.




###### Para mejor visualización consulte <a href = "anexo\styles.css"><i>styles.css</i></a>


## Creación del `script.js`


Para la creación del `script.js` seguimos los siguientes pasos:


### 1. Manejo del tema oscuro/claro


<!-- #region -->
```js
// Toggle para modo oscuro/claro
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Comprobar preferencia del sistema
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// Comprobar si hay preferencia guardada
const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
    body.classList.add('dark-mode');
    themeToggle.textContent = 'Modo Claro';
}

themeToggle.addEventListener('click', function() {
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        themeToggle.textContent = 'Modo Claro';
        localStorage.setItem('theme', 'dark');
    } else {
        themeToggle.textContent = 'Modo Oscuro';
        localStorage.setItem('theme', 'light');
    }
});
```
<!-- #endregion -->

**Implementa la funcionalidad de alternancia entre modos oscuro y claro.** Verifica la preferencia del sistema y el tema guardado en `localStorage`. Al hacer clic en el botón:
- **Alterna** la clase `dark-mode` en el cuerpo del documento
- **Actualiza** el texto del botón según el modo activo
- **Guarda** la preferencia del usuario en `localStorage` para persistencia


### 2. Reinicio de filtros

<!-- #region -->
```js
// Botón para reiniciar filtros
document.getElementById('reset-btn').addEventListener('click', function() {
    // Quitar todos los parámetros de la URL
    window.location.href = window.location.pathname;
});
```
<!-- #endregion -->

**Gestiona el reinicio de los filtros del dashboard.** Al hacer clic en el botón de reinicio:
- **Redirige** al usuario a la URL base sin parámetros de consulta
- **Elimina** todos los filtros aplicados actualmente
- **Restaura** la vista inicial del dashboard


###### Para mejor visualización consulte <a href = "anexo\script.js"><i>script.js</i></a>


# Implementación de dashboard web interactivo


Con tal de poder interactuar con el dashboard desde distintos dispositivos, decidimos crear una webapp con Flask dentro de <a href = "https://www.pythonanywhere.com/"><i>pythonanywhere.com</i></a>.

Para la creación de nuestra webapp, seguimos el siguiente procedimiento:


## 1. Creamos la base de datos


<img src = "media\4. DBCreacion.png">


## 2. Cargamos el archivo .sql dentro de nuestros archivos de pythonanywhere.com


<img src = "media\4.1 SQL.jpg">


## 3. Cargamos los datos dentro de nuestra base de datos MySQL


<img src = "media\4.2 Carga.png">


## 4. Revisamos las tablas que se crearon dentro de la base de datos


<img src = "media\4.3 Tables.png">


## 5. Checamos la cantidad de registros dentro de la tabla DIM_ASISTENCIAS, DIM_MATERIAS Y HECHOS_DEMOGRAFICOS


<img src = "media\4.4 Asistencias.png">


<img src = "media\4.5 Materias.png">


<img src = "media\4.6 Datos demograficos.png">


## 6. Creamos nuestra webapp


<img src = "media\5. Creamos webapp.png">


## 7. Establecemos la jerarquia de los archivos


```
/
├── flask_app.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       └── dashboard.png
└── templates/
    └── dashboard.html
```


<img src = "media\5.2.1 Jerarquia.jpg">


<img src = "media\5.2.2 Jerarquia.jpg">


<img src = "media\5.2.3 Jerarquia.jpg">


<img src = "media\5.2.4 Jerarquia.jpg">


<img src = "media\5.2.5 Jerarquia.jpg">


<img src = "media\5.2.6 Jerarquia.jpg">


## 8. Instalamos dependencias


Instalamos las siguientes dependencias dentro de un entorno virtual `flask, flask_sqlalchemy, sqlalchemy, bokeh` y `pandas`


<img src = "media\5.3 Instalamos dependencias.png">


posteriormente, también se realiza la instalación de `mysqlclient`


<img src = "media\5.3.2 Dependencias.png">


## 9. Subimos el código de nuestra `flask_app.py`


<img src = "media\6.1 App.jpg">


## 10. Subimos el código de nuestro `dashboard.html`


<img src = "media\6.2 Html.jpg">


## 11. Subimos nuestro `styles.css`


<img src = "media\6.3 css.jpg">


## 12. Subimos nuestro `script.js`


<img src = "media\6.4 js.jpg">


## 13. Apuntamos la ruta del entorno virtual que usamos, dentro de la configuración de la app


<img src = "media\5.6 Configurar entorno virtual.png">


## 12. Observamos el resultado inicial


<img src = "media\8. Resultado inicial.jpg">


###### El dashboard se encuentra disponible en: <a><i>https://fedivej259.pythonanywhere.com/</i></a>


# Repositorio


Almacenamos los archivos fuente de nuestra actividad dentro de: <a><i>https://github.com/acamacho0723/dags-etl-23062025</i></a>
