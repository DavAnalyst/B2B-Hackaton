import subprocess

def run_script(script_name):
    """Ejecuta un script Python dado en el sistema."""
    try:
        print(f"Ejecutando {script_name}...")
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}: {e}")
        print(e.stderr)

if __name__ == "__main__":
    # Ejecutar los scripts en orden
    run_script('scrap.py')       # Paso 1: Ejecutar el scraping
    run_script('insertData.py')  # Paso 2: Insertar los datos en la base de datos
    run_script('app.py')         # Paso 3: Ejecutar la aplicación Streamlit
