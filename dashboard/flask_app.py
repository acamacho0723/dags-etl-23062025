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
        
        # Depuración: Verificar datos obtenidos
        print(f"Registros obtenidos para gráfico de barras: {len(df_barras)}")
        print(df_barras.head())
        
        if not df_barras.empty:
            df_barras['promedio'] = df_barras['promedio'].astype(float)
            df_barras['semestre'] = df_barras['semestre'].astype(str)
            
            # Ordenar por semestre y materia
            df_barras = df_barras.sort_values(['semestre', 'materia'])
            
            # Preparar datos para gráfica de barras horizontales
            data = {
                'materia_genero': [],
                'semestre': [],
                'promedio': [],
                'genero': [],
                'color': [],
                'semestre_label': []  # Para las etiquetas de semestre
            }
            
            # Paleta de colores por género
            color_map = {
                'F': Category10[3][0],
                'M': Category10[3][1]
            }
            
            # Variables para seguimiento de semestres
            current_semestre = None
            semestre_positions = {}
            semestre_materias = defaultdict(list)
            
            # Agrupar materias por semestre
            for semestre in df_barras['semestre'].unique():
                semestre_materias[semestre] = df_barras[df_barras['semestre'] == semestre]['materia'].unique().tolist()
            
            # Llenar los datos y calcular posiciones para separadores
            for idx, row in df_barras.iterrows():
                materia_gen = f"{row['materia']} - {row['genero']}"
                
                # Verificar si es un nuevo semestre
                if row['semestre'] != current_semestre:
                    current_semestre = row['semestre']
                    semestre_positions[current_semestre] = len(data['materia_genero'])
                
                data['materia_genero'].append(materia_gen)
                data['semestre'].append(row['semestre'])
                data['promedio'].append(row['promedio'])
                data['genero'].append(row['genero'])
                data['color'].append(color_map[row['genero']])
                data['semestre_label'].append('')
            
            # Agregar espacio extra después de cada semestre
            espacios_extra = []
            for semestre in semestre_positions:
                if semestre != list(semestre_positions.keys())[-1]:
                    espacios_extra.append(semestre_positions[semestre] + len(semestre_materias[semestre]) - 1)
            
            source_barras = ColumnDataSource(data)
            
            # Herramientas interactivas
            herramientas_barras = [
                'pan', 'wheel_zoom', 'box_zoom', 'reset', 'save', 'hover'
            ]
            
            # Crear figura con barras HORIZONTALES
            p1 = figure(
                y_range=data['materia_genero'],
                x_range=Range1d(0, 120),  # Ampliar rango para etiquetas
                title="Promedio por Materia y Género",
                height=800,
                width=1000,
                tools=herramientas_barras,
                toolbar_location="above",
                y_axis_label="Materia y Género",
                x_axis_label="Promedio (%)"
            )
            
            # Configurar etiquetas del eje Y (horizontal)
            p1.yaxis.major_label_orientation = 0  # 0 grados (horizontal)
            p1.yaxis.major_label_text_font_size = "10pt"
            
            # Crear renderizadores para cada género
            r = p1.hbar(
                y='materia_genero',
                right='promedio',
                height=0.7,
                source=source_barras,
                fill_color='color',
                line_color='darkgrey',
                alpha=0.9,
                name='genero',
                muted_alpha=0.1
            )
            
            # Configurar hover
            hover_barras = p1.select_one(HoverTool)
            hover_barras.tooltips = [
                ("Materia", "@materia_genero"),
                ("Semestre", "@semestre"),
                ("Promedio", "@promedio{0.00}%")
            ]
            hover_barras.mode = 'mouse'
            
            # CORRECCIÓN: Crear leyenda con cuadrados visibles
            legend_items = []
            generos_presentes = set(data['genero'])
            
            for genero in generos_presentes:
                if genero in color_map:
                    # Crear un glifo visible para la leyenda
                    r_legend = p1.square(
                        x=[-100], y=[-100], 
                        size=15, 
                        fill_color=color_map[genero],
                        line_color='black',
                        alpha=1.0,
                        name=f'legend_{genero}'
                    )
                    # Hacer invisible pero mantener color en leyenda
                    r_legend.visible = False
                    legend_items.append(LegendItem(label=genero, renderers=[r_legend]))
            
            if legend_items:
                legend = Legend(
                    items=legend_items,
                    location="top_right",
                    click_policy="mute"
                )
                p1.add_layout(legend, 'right')
            
            # Añadir separadores de semestre con espacio extra
            for i, (semestre, position) in enumerate(semestre_positions.items()):
                # Calcular posición final del semestre
                materias_sem = semestre_materias[semestre]
                num_materias = len(materias_sem)
                end_position = position + num_materias * 2 - 1  # 2 barras por materia
                
                # Ajuste clave: Mover el delimitador DOS BARRAS HACIA ABAJO
                separator_pos = end_position + 1.0  # Espacio reducido para evitar cortes
                
                # Añadir línea separadora SOLO si no es el último semestre
                if i < len(semestre_positions) - 1:
                    separator = Span(
                        location=separator_pos, 
                        dimension='width', 
                        line_color='black', 
                        line_width=1.5, 
                        line_dash='dashed'
                    )
                    p1.add_layout(separator)
                
                # Añadir etiqueta de semestre CENTRADA en el grupo, a la derecha
                center_pos = (position + end_position) / 2
                p1.text(
                    x=105,  # Posicionado a la derecha de las barras
                    y=center_pos,
                    text=[f"S{semestre}"],  # Formato: S1, S2, etc.
                    text_font_size="12pt",
                    text_font_style="bold",
                    text_color="navy",
                    text_align="left",  # Alineado a la izquierda
                    text_baseline="middle"
                )
            
            # Ajustar aspecto visual
            p1.xgrid.grid_line_color = None
            p1.x_range.start = 0
            p1.ygrid.grid_line_color = None
            
            # Aumentar margen izquierdo para etiquetas
            p1.min_border_left = 300
            
        else:
            # Crear figura vacía si no hay datos
            p1 = figure(
                title="Promedio por Materia y Género",
                height=300,
                width=800,
                toolbar_location=None
            )
            p1.xaxis.axis_label = "Promedio (%)"
            p1.yaxis.axis_label = "Materia y Género"
            p1.text(
                x=[0.5], y=[0.5], 
                text=["No hay datos disponibles con los filtros seleccionados"],
                text_align="center", text_baseline="middle"
            )

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
        
        # Crear objeto text con bindparams para expansión
        query2 = text(query_text2)
        if bind_params:
            query2 = query2.bindparams(*bind_params)
        
        result2 = db.session.execute(query2, parametros)
        df_disp = pd.DataFrame(result2, columns=['promedio', 'asistencia', 'materia', 'semestre', 'genero'])
        
        # Depuración: Verificar datos obtenidos
        print(f"Registros obtenidos para gráfico de dispersión: {len(df_disp)}")
        print(df_disp.head())
        
        if not df_disp.empty:
            df_disp['promedio'] = df_disp['promedio'].astype(float)
            df_disp['asistencia'] = df_disp['asistencia'].astype(float)
            # Crear columna para tooltip
            df_disp['info'] = df_disp.apply(
                lambda row: f"{row['materia']} - S{row['semestre']} - {row['genero']}", 
                axis=1
            )
            
            # Preparar colores por género
            color_map_disp = {
                'F': Category10[3][0],
                'M': Category10[3][1]
            }
            df_disp['color'] = df_disp['genero'].map(color_map_disp)
            
            source_disp = ColumnDataSource(df_disp)
        else:
            # Crear dataframe vacío con estructura completa
            df_disp = pd.DataFrame(columns=['promedio', 'asistencia', 'info', 'color'])
            source_disp = ColumnDataSource(df_disp)
        
        # Herramientas interactivas
        herramientas_disp = [
            'pan', 'wheel_zoom', 'box_zoom', 'reset', 'save', 'hover'
        ]
        
        p2 = figure(
            title="Promedio vs Asistencia",
            height=500,
            width=800,
            tools=herramientas_disp,
            toolbar_location="above"
        )
        
        if not df_disp.empty:
            scatter = p2.scatter(
                'promedio',
                'asistencia',
                size=10,
                alpha=0.6,
                color='color',
                source=source_disp,
                legend_field='genero'
            )
            
            # Hacer la leyenda interactiva
            p2.legend.click_policy = "mute"
            p2.legend.location = "top_left"
            p2.legend.title = "Género"
        
        # Configuración de ejes
        p2.xaxis.axis_label = "Promedio General"
        p2.yaxis.axis_label = "Porcentaje de Asistencia"
        p2.x_range = Range1d(0, 100)
        p2.y_range = Range1d(0, 100)
        p2.xgrid.grid_line_color = None
        p2.ygrid.grid_line_alpha = 0.3
        
        # Configurar hover
        hover_disp = p2.select_one(HoverTool)
        hover_disp.tooltips = [
            ("Materia/Semestre/Género", "@info"),
            ("Promedio", "@promedio{0.00}"),
            ("Asistencia", "@asistencia{0.00}%")
        ]

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
    
    # Agrupar materias por semestre
    materias_por_semestre = {}
    for row in result:
        semestre = str(row.SEMESTRE)
        if semestre not in materias_por_semestre:
            materias_por_semestre[semestre] = []
        materias_por_semestre[semestre].append((row.materia_id, row.nombre_materia))
    
    # Convertir a lista de tuplas (semestre, materias)
    materias_agrupadas = [
        (semestre, materias_por_semestre[semestre]) 
        for semestre in sorted(materias_por_semestre.keys(), key=lambda s: int(s), reverse=True)
    ]
    
    return materias_agrupadas

if __name__ == '__main__':
    app.run(debug=True)
