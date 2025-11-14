# Automatización Dropi - Pipeline ETL

## 📋 Descripción

Este proyecto es un sistema automatizado de extracción, transformación y carga (ETL) que obtiene datos de la plataforma **Dropi** (plataforma de e-commerce) mediante web scraping, los procesa en un pipeline de tres capas (Bronze, Silver, Gold) y los almacena en una base de datos DuckDB para generar reportes de ventas generales.

### Funcionalidad Principal

El sistema automatiza la extracción de los siguientes datos desde Dropi:
- **Órdenes** (una orden por fila y órdenes con productos)
- **Garantías**
- **Historial de Cartera**
- **Devoluciones**

Posteriormente, procesa estos datos a través de un pipeline de tres capas:
1. **Bronze (Capa Raw)**: Almacena los datos extraídos sin procesar
2. **Silver (Capa Limpia)**: Limpia y transforma los datos raw
3. **Gold (Capa Final)**: Genera agregaciones y reportes finales

El resultado final es un archivo CSV (`general_sales.csv`) con un reporte consolidado de ventas generales.

## 🚀 Requisitos Previos

- **Python 3.12** o superior
- **Navegador Chrome** instalado (para Selenium)
- **Cuenta de Dropi** con credenciales de acceso
- **Conexión a Internet** (para acceder a Dropi y descargar datos)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd DROPO_ETL_Pipeline
```

### 2. Crear y activar el entorno virtual

**En Windows:**
```bash
python -m venv dropi-extractor-venv
dropi-extractor-venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv dropi-extractor-venv
source dropi-extractor-venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DROPI_USER=tu_usuario_dropi
DROPI_PASS=tu_contraseña_dropi
DROPI_SHEETS_ID=id_de_google_sheets_opcional
```

**Nota**: El archivo `.env` no debe subirse al repositorio por seguridad.

### 5. Verificar archivos necesarios

Asegúrate de que exista el archivo de credenciales de Google Sheets (si se requiere):
- `assets/anakarinadropi-572e7897ef4c.json`

## ▶️ Ejecución

### ⚠️ Primera Ejecución - Inicialización Automática

**Si es la primera vez que ejecutas el proyecto**, el sistema realizará automáticamente:

1. **Creación de la base de datos**: Se creará automáticamente el archivo `db/Oferfly.duckdb` en la carpeta `db/`
2. **Creación de todas las tablas**: Se ejecutará el script de inicialización (`db/init_tables.py`) que creará todas las tablas necesarias:
   - **Tablas RAW (Bronze)**: `RAW_ORDERS`, `RAW_ORDERS_PRODUCTS`, `RAW_WARRANTYS`, `RAW_WALLET`, `RAW_DEVOLUTIONS`
   - **Tablas finales (Silver/Gold)**: `ORDERS`, `ORDERS_PRODUCT`, `WARRANTYS`, `WALLET`, `DEVOLUTIONS`, `GENERAL_SALES`

**Nota importante**: 
- La inicialización es automática y se ejecuta cada vez que corres el pipeline
- Solo crea las tablas que no existen, por lo que es seguro ejecutarlo múltiples veces
- Si alguna tabla ya existe, el sistema la detectará y no la recreará
- Los logs mostrarán qué tablas se crearon y cuáles ya existían

### Ejecutar el pipeline completo

Desde la raíz del proyecto, ejecutar:

```bash
python main.py
```

El script ejecutará automáticamente los tres pasos del pipeline:
1. `pipeline.run_bronze_pipeline` - Extracción y carga de datos raw
2. `pipeline.run_silver_pipeline` - Transformación y limpieza de datos
3. `pipeline.run_gold_pipeline` - Generación del reporte final

### Salida esperada

Al finalizar la ejecución, encontrarás:
- **Base de datos**: `db/Oferfly.duckdb` (DuckDB con todas las tablas procesadas - se crea automáticamente en la primera ejecución)
- **Reporte CSV**: `data/general_sales.csv` (reporte final de ventas generales)

## 📁 Estructura del Proyecto

```
NUEVA_Automatizacion_Dropi/
├── assets/                    # Archivos de configuración (credenciales Google Sheets)
├── data/                      # Datos de salida (CSV generados)
├── db/                        # Base de datos DuckDB y queries SQL
│   ├── querys/               # Scripts SQL para crear tablas y upserts
│   ├── init_tables.py         # Script de inicialización de tablas (se ejecuta automáticamente)
│   └── Oferfly.duckdb        # Base de datos (se crea automáticamente)
├── dropi_logic/              # Lógica de extracción (RPA, scraping, Google Sheets)
├── pipeline/                 # Pipeline ETL (extract, transform, load)
├── validations/              # Validaciones de datos
├── config.py                 # Configuración centralizada
├── main.py                   # Punto de entrada principal
├── requirements.txt          # Dependencias del proyecto
└── .env                      # Variables de entorno (crear manualmente)
```

## 🔄 Flujo del Pipeline

### 1. Bronze Pipeline
- **Extracción**: Utiliza Selenium para hacer web scraping en Dropi y descargar reportes Excel
- **Carga**: Almacena los datos sin procesar en tablas RAW (RAW_ORDERS, RAW_ORDERS_PRODUCTS, RAW_WARRANTYS, RAW_WALLET, RAW_DEVOLUTIONS)

### 2. Silver Pipeline
- **Extracción**: Obtiene los datos de la última ingesta de la capa Bronze
- **Transformación**: 
  - Limpia y valida los datos
  - Normaliza formatos de fechas
  - Transforma estados de órdenes
  - Separa campos compuestos
- **Carga**: Almacena datos procesados en tablas finales (ORDERS, ORDERS_PRODUCT, WARRANTYS, WALLET, DEVOLUTIONS)

### 3. Gold Pipeline
- **Extracción**: Obtiene datos agregados de la capa Silver
- **Validación**: Valida datos numéricos y nulos
- **Carga**: Genera tabla consolidada GENERAL_SALES y exporta a CSV

## ⚙️ Configuración

El archivo `config.py` contiene toda la configuración del proyecto:
- Rutas de directorios
- Configuración de base de datos
- Tipos de datos para DataFrames
- Mapeo de estados de órdenes
- Configuración de scraping y Google Sheets

## 📊 Tablas de la Base de Datos

### Capa Bronze (RAW)
- `RAW_ORDERS`
- `RAW_ORDERS_PRODUCTS`
- `RAW_WARRANTYS`
- `RAW_WALLET`
- `RAW_DEVOLUTIONS`

### Capa Silver/Gold
- `ORDERS`
- `ORDERS_PRODUCT`
- `WARRANTYS`
- `WALLET`
- `DEVOLUTIONS`
- `GENERAL_SALES`

## 🔍 Logs

El sistema genera logs detallados durante la ejecución con el siguiente formato:
```
YYYY-MM-DD HH:MM:SS - LEVEL - Mensaje
```

Los logs incluyen información sobre:
- Inicio y fin de cada paso del pipeline
- Errores y advertencias
- Progreso de descargas y procesamiento

## ⚠️ Notas Importantes

1. **Tiempo de ejecución**: El proceso completo puede tardar varios minutos debido a:
   - Web scraping (requiere esperar descargas de archivos Excel)
   - Procesamiento de datos
   - Validaciones

2. **Navegador**: El sistema utiliza Chrome con Selenium. Asegúrate de tener Chrome instalado y actualizado.

3. **Carpeta de Descargas**: Los archivos Excel se descargan temporalmente en la carpeta `Downloads` del usuario y luego se procesan.

4. **Base de Datos**: La base de datos DuckDB (`db/Oferfly.duckdb`) y todas las tablas se crean automáticamente en la primera ejecución mediante el script `db/init_tables.py`. No es necesario crear manualmente la base de datos ni las tablas.

## 🐛 Solución de Problemas

### Error: "El ejecutable de Python no fue encontrado"
- Verifica que el entorno virtual esté creado correctamente
- Asegúrate de que el nombre del venv sea `dropi-extractor-venv`

### Error: "Variables de entorno no encontradas"
- Verifica que el archivo `.env` exista en la raíz del proyecto
- Confirma que las variables `DROPI_USER` y `DROPI_PASS` estén configuradas

### Error: "ChromeDriver no encontrado"
- El proyecto usa `webdriver-manager` que descarga automáticamente el driver
- Verifica tu conexión a Internet

### Error en la descarga de archivos
- Verifica tu conexión a Internet
- Confirma que las credenciales de Dropi sean correctas
- Revisa que la carpeta `Downloads` sea accesible

## 📝 Dependencias Principales

- **selenium**: Web scraping automatizado
- **pandas**: Procesamiento de datos
- **duckdb**: Base de datos analítica
- **openpyxl**: Lectura de archivos Excel
- **python-dotenv**: Gestión de variables de entorno
- **google-api-python-client**: Integración con Google Sheets (opcional)

## 👤 Autor

Proyecto desarrollado por Leonardo Polanco


