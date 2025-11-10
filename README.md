# ⚙️ ELT Dropi Data Pipeline - Integración y Verificación de Órdenes 📊

Este proyecto implementa un **ELT** (Extract, Load, Transform) para la consolidación de reportes de la plataforma **Dropi**. Utiliza una solución de **RPA** para la descarga automatizada de reportes y un *pipeline* de procesamiento de datos en capas **Raw**, **Silver** y **Gold**.

---

## 🚀 Objetivo Principal

El propósito central del *pipeline* es **consolidar y evaluar la trazabilidad y la liquidación financiera** de cada orden. El objetivo final es generar un archivo maestro único que permita:

1.  Determinar el **estado real** y la **trazabilidad completa** de cada orden.
2.  Calcular el **monto neto pagado** (entradas menos salidas) por orden.
3.  Verificar si la **liquidación** (el pago final) fue correcta, especialmente en el caso de las órdenes **entregadas** y **devueltas**.

---

## 🛠️ Flujo del Proceso (ELT)

El proceso se divide en la ingesta, limpieza y transformación, siguiendo una arquitectura de capas de datos:

### 1. Extracción y Carga (E & L) - Capa **Raw**

* **RPA:** Una herramienta de automatización robótica accede a la cuenta de **Dropi** y descarga los siguientes reportes diarios:
    * Órdenes
    * Devoluciones
    * Garantías
    * Historial de Cartera
* **Carga:** Los reportes descargados se cargan directamente a la capa **Raw** (datos sin procesar).

### 2. Transformación I - Capa **Silver**

Esta capa se enfoca en la **limpieza** y **preparación** de los datos antes de la consolidación.

* Se realiza la **limpieza de espacios en blanco** en los campos de texto.
* Los reportes acumulativos (ej. Historial de Cartera) se actualizan **fusionando** el archivo más reciente con el histórico, asegurando que **no haya duplicidad** de información y manteniendo solo el registro más antiguo hasta la fecha del nuevo reporte.

### 3. Transformación II - Capa **Gold** (Consolidación)

Esta es la capa final donde se aplica la lógica de negocio para generar el archivo maestro consolidado, uniendo toda la información.

* **Inicio con Órdenes:** La lista de órdenes sirve como punto de partida. Se **estandarizan los estados** de la orden (ej., 'Completada' y 'Finalizada' se unifican).
* **Añadir Garantías:** Se agrupan y se añaden todos los **códigos de garantía** asociados a cada orden en una sola celda.
* **Añadir Historial de Pagos:** Se determina la **fecha más reciente** de pago y se calcula el **monto total pagado neto** (sumando 'Entradas' y restando 'Salidas').
* **Añadir Devoluciones:** Se registra la fecha y el ID del registro de devolución si aplica.
* **Chequeo de Verificación (Liquidación):** Se aplica una lógica de negocio para evaluar la liquidación:
    * Si la orden está **ENTREGADA**, se compara el monto esperado *versus* el monto pagado. Si coinciden, es **"OK"**, si no **"POR REVISAR"**.
    * Si la orden está **DEVUELTA**, se valida la existencia de la fecha de devolución. Si existe, es **"OK"**, si no **"POR REVISAR"**.

* **Mantenimiento de la Base Maestra:** El *dataframe* consolidado se utiliza para actualizar el archivo maestro final:
    * Se añaden las **órdenes nuevas**.
    * Se actualizan los datos de las **órdenes existentes**.
    * Se mantiene un **historial de estados** para cada orden, registrando la fecha del último cambio de estado.

---

## ⚠️ Estado del Proyecto

Este proyecto **no está completamente finalizado** y se encuentra en fase de desarrollo activo.

### 📌 Tareas Pendientes:

* Validar que la actualización de las columnas de **fecha y hora (*timestamp*)** sea correcta.
* Incluir el campo **`update_at`** en la información general de ventas.
* **Validar** que las rutas de archivos funcionen correctamente en un entorno **Linux**.
* Implementar el **Monitoreo de Logging** y los **Logs de inserción** completos.
