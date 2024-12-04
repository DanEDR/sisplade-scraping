from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import csv
import re
import logging

# Configuración de logging
logging.basicConfig(
    filename='scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Expresiones regulares para extraer datos
regex_mun = re.compile(r'^Municipio de (.*)$')
regex_income = re.compile(r"^\$\s*(.*)$")

# URL base del sitio web
URL_BASE = 'https://sisplade.oaxaca.gob.mx/sisplade/smIngresosMunicipio.aspx?idMunicipio='

"""
def get_year(soup, i):
    
    Extrae el año de la pestaña activa.
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup del HTML actual.
        i (int): Índice de la pestaña.
    Returns:
        int: Año correspondiente a la pestaña.
    
    tag_a = soup.select_one(f'#ContentPlaceHolder1_tabEjercicios_AT{i}T')
    return int(tag_a.text)
"""

def get_municipio(soup):
    """
    Extrae el nombre del municipio desde el HTML.
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup del HTML actual.
    Returns:
        str: Nombre del municipio.
    """
    municipio = soup.select_one('#ContentPlaceHolder1_lblMunicipio').text
    return regex_mun.match(municipio).group(1)

def get_income(soup):
    """
    Extrae el ingreso total del HTML analizado.
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup del HTML actual.
    Returns:
        str: Ingreso total.
    """
    main_div = soup.select_one('div.col-lg-9')
    income = main_div.div.span.b.text
    return regex_income.match(income).group(1)


def get_income_by_year(driver, records):
    """
    Extrae los ingresos por año y los añade al registro.
    Args:
        driver (webdriver.Chrome): Driver de Selenium.
        records (dict): Estructura de datos para almacenar los registros.
    Returns:
        dict: Registros actualizados con los ingresos.
    """
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        municipio = get_municipio(soup)
        records['Municipio'].append(municipio)
        
        income = get_income(soup)
        records[2021].append(income)
        
        logging.info(f'Procesando los datos del municipio de {municipio}')
        
        for i in range(1, 7):
            id = f'ContentPlaceHolder1_tabEjercicios_T{i}T'
            try:
                driver.find_element(By.ID, id).click()    
                Wait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblTextoFISMDF'))
                )
                
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                #year = get_year(soup, i)
                income = get_income(soup)
                records[2014 + i].append(income)

                #logging.info(f'{year} -> {income}')
            except (Exception):
                logging.error(f'Error en el año {2015 + i - 1} del municipio {municipio}')
                records[2015 + i - 1].append(None)
    except Exception as e:
        logging.error(f"Error al procesar el municipio: {e}")
    
    return records

def create_file_sisplade_csv(data):
    '''
    Crea un archivo CSV con los datos extraídos.
    Args:
        data (dict): Diccionarip con los registros de los ingresos.
    '''
    headers = list(data.keys())
    values = list(zip(*data.values()))
    
    try:
        with open('../data/ingresos_por_municipio.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(values)
        logging.info('Archivo CSV generado exitosamente.')
    except Exception as e:
        logging.error(f'Error al crear el archivo CSV: {e}')
        
def data_structure(start_year=2015, end_year=2021):
    '''
    Inicializa la estructura de datos para almacenar los registros.
    Args:
        initial_year (int): Año en el que comienza el almacenamiento de los ingresos.
        final_year (int): Año en el que finaliza el almacenamiento de los ingresos.
    Returns:
        dict: Estructura de datos con las claves iniciales.
    '''
    data = {'id':[], 'Municipio':[]}
    for year in range(start_year, end_year + 1):
        data[year] = []
    return data

def main():
    '''
    Función principal que realiza el scraping y genera el archivo CSV.
    '''
    # Configuración del driver de Selenium
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')    # Ejecución en modo headless (sin ventana gráfica)
    options.add_argument('--disable-gpu') # Desactivar aceleración de GPU
    options.add_argument('--log-livel=3') #Reducir logs de Chromium
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        data = data_structure()
        
        # Iterar sobre los municipios
        for idmunicipio in range(1, 571): #Ajustar el rango según el número de municipio que desee extraer (1-570).
            URL_FINAL = f'{URL_BASE}{idmunicipio}'
            data['id'].append(idmunicipio)
            
            try:
                driver.get(URL_FINAL)
                data = get_income_by_year(driver, data)
            except Exception as e:
                logging.error(f'Error al procesar el municipio con ID {idmunicipio}: {e}')
                continue
        
        # Crear el archivo CSV con los datos
        create_file_sisplade_csv(data)
    except Exception as e:
        logging.error(f'Error en la ejecución principal: {e}')
    finally:
        driver.quit()
        logging.info('Ejecución finalizada. Selenium cerrado.')
        
if __name__ == '__main__':
    main()