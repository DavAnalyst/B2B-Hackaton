import streamlit as st
import pandas as pd
import mysql.connector
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import plotly.express as px
from graphviz import Digraph

username = 'root'
password = 'nievedinho.123'
host = 'localhost'
database = 'db_proveedores'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

# Consulta SQL
sql = """
    SELECT *
    FROM tsol
    WHERE 
        YEAR(`FEC-RENOVACION`) >= 2020 
        AND `EST-MATRICULA` IN ('IA', 'MA') 
        AND `NIT` IS NOT NULL
        AND `CIIU-1` NOT LIKE %s
        AND `CIIU-1` NOT LIKE %s
        AND `CIIU-1` NOT LIKE %s;
"""

# Leer los datos y convertirlos a un DataFrame
params=("%menor%","%dentro del establecimiento%","%a la mesa%")
df = pd.read_sql(sql, engine,params=params)
df['TAM-EMPRESA'] = df['TAM-EMPRESA'].replace(['N',np.nan], 'Otros')

print(df.info())

# Título de la app
st.title('BUSCADOR B2B TRADE MATCH')

st.write("""
    ESTA APLICACION PERMITE BUSCAR PROVEEDORES B2B EN ANTIOQUIA
""")

# Filtros interactivos
st.header('Filtros de Búsqueda')

# Filtro para "CIIU-1" (usando multiselect si quieres permitir múltiples selecciones)
ciiu_options = df['CIIU-1'].unique()
ciiu_filter = st.selectbox('PORTAFOLIO DE PRODUCTOS Y SERVICIOS', ciiu_options,index=0)

# Filtro para "MUN-COMERCIAL" (usando selectbox para una sola opción)
mun_options = df['MUN-COMERCIAL'].unique()
mun_filter = st.selectbox('SELECCION MUNICIPIO', mun_options, index=0)

# Filtro para "TAM-EMPRESA" (usando selectbox para una sola opción)
tam_options = df['TAM-EMPRESA'].unique()
tam_filter = st.selectbox('TAMAÑO DE LA EMPRESA', tam_options, index=0)

# Aplicar los filtros
df_filtered = df[
    (df['CIIU-1'] == (ciiu_filter)) & 
    (df['MUN-COMERCIAL'] == mun_filter) &
    (df['TAM-EMPRESA'] == tam_filter)
]

# Mostrar los datos filtrados
st.header('Proveedores Activos Filtrados')
st.write(df_filtered)

st.header('Contacto del Proveedor')
st.write(df_filtered["TEL-COM-1"])

# Visualización: Gráfico de barras de la distribución de TAM-EMPRESA
fig_tam_empresa = px.bar(df_filtered,   
                         x='ORGANIZACION', 
                         title='Distribución Tipo de Organizacion',
                         labels={'ORGANIZACION': 'Tipo de Organizacion', 'count': 'Cantidad'},
                         color='ORGANIZACION')

st.plotly_chart(fig_tam_empresa)

# Título de la aplicación
st.title("Flujo de Trabajo TradeMatch")

# Crear el objeto Digraph de Graphviz
dot = Digraph()

# Agregar nodos al diagrama
dot.node('A', 'Inicio')
dot.node('B', 'Scraping Dian Region Antioquia')
dot.node('C', 'Analisis Bases de Datos Utiles')
dot.node('D', 'Carga de Datos a BD Mysql')
dot.node('E', 'Consulta y Limpieza de Datos')
dot.node('E', 'Generacion de App Streamli')

# Conectar los nodos (flechas)
dot.edge('A', 'B', label='Inicia el proceso')
dot.edge('B', 'C', label='Extraccion y Carga')
dot.edge('C', 'D', label='Limpieza')
dot.edge('D', 'E', label='Gráficos generados')

# Mostrar el diagrama en Streamlit
st.graphviz_chart(dot)
