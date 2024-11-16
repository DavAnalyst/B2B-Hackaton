import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def tsol():
    # Leer el archivo Excel
    df = pd.read_csv(r"C:\Users\equip\Downloads\BASE_DE_DATOS_PYMES_CCMMNA_20241115.csv")

    # Reemplazar valores NaN con None
    df.replace({np.nan: None}, inplace=True)

    # Configurar la conexión a MySQL usando SQLAlchemy
    username = 'root'
    password = 'nievedinho.123'
    host = 'localhost'
    database = 'db_proveedores'

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

    try:
        # Subir el DataFrame a MySQL
        df.to_sql(
            name='tsol',         # Nombre de la tabla
            con=engine,          # Conexión a la base de datos
            if_exists='replace', # Reemplaza la tabla si ya existe (cambiar a 'append' para agregar datos)
            index=False          # No guardar el índice como columna
        )
        print("Datos insertados y columnas creadas correctamente.")
    except Exception as e:
        # Manejo de errores
        print(f"Error al insertar datos: {e}")
    finally:
        # Cerrar la conexión
        engine.dispose()
tsol()