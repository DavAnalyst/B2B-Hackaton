from bs4 import BeautifulSoup
import requests

# URL base sin el número de página
url_dian = "https://www.datos.gov.co/browse?Informaci%C3%B3n-de-la-Entidad_Departamento=Antioquia&amp%3Ban=&amp%3Butf8=%E2%9C%93&category=Comercio%2C+Industria+y+Turismo&limitTo=datasets&sortBy=relevance&page="
page = 1
hay_resultados = True

while hay_resultados:
    # Construir la URL con el número de página actual
    url = f"{url_dian}{page}"
    
    # Obtener el contenido de la página actual
    respuesta = requests.get(url)
    html = respuesta.text
    soup = BeautifulSoup(html, "html.parser")

    # Encontrar todos los elementos con la clase 'browse2-result-name-link'
    resultados = soup.find_all(class_="browse2-result-name-link")

    # Verificar si hay resultados en la página actual
    if resultados:
        print(f"\nPágina {page} - Resultados encontrados:")
        # Imprimir el texto de cada elemento encontrado
        for resultado in resultados:
            print(resultado.text.strip())
        
        # Pasar a la siguiente página
        page += 1
    else:
        # Si no hay resultados, finalizar el bucle
        hay_resultados = False
        print("\nNo hay más resultados.")
        
