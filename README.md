# Extracción de datos al sitio web SISPLADE

## Descripción
Este proyecto extrae información del sitio web SISPLADE, donde se encuentran los registros de ingresos y egresos de cada municipio de Oaxaca. El objetivo es obtener los ingresos municipales entre 2015 y 2021. Los datos se almacenan en un archivo CSV, en el cual cada fila representa el ingreso anual de cada municipio.

## Instalación
Clona este repositorio y crea el entorno:
```bash
git clone https://github.com/DanEDR/sisplade-scraping.git
cd sisplade-scraping
mamba env create -f environment.yml
```
Activa el entorno:
```bash
mamba activate scraping_env
```

## Uso
Ejecuta el script principal
```bash
pyhton scripts/main.py
```
Esto generará el archivo `data/ingresos_por_municipio.csv`

## Estructura del proyecto
A continuación se muestra la estructura del proyecto:

├── README.md                       <!-- # Documentación -->
├── data                            <!-- # Carpeta donde se guardan los datos extraídos -->  
│   └── ingresos_por_municipio.csv  <!-- # Archivo con los datos extraídos -->
├── environment.yml                 <!-- # Configuración de entorno -->
└── scripts                         <!-- # Archivos de código fuente-->
    └── scraping.py                 <!-- # Script de extracción-->

## Resultados

Los ingresos municipales extraídos incluyen:

- **Periodo**: 2015 - 2021.
- **Formato**: CSV con columnas para id, municipio y años.

### Ejemplo del contenido:

| id | Municipio | 2015       | 2016       | 2017       | 2018       | 2019       | 2020       | 2021       |
|----|-----------|------------|------------|------------|------------|------------|------------|------------|
| 1  | Abejones  | 8,400,543| 8,858,575| 12,918,488| 9,267,467| 10,093,756| 10,208,254| 29,564,212|

## Tecnoligías utilizadas
- **Pyhton**
- **Selenium**
- **Beautifulsoup**
- **mamba** (para la gestión de entornos)

## Proyecto futuro
En un futuro los datos obtenidos en este proyecto se analizaran en detalle.
