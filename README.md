_Realizar CheckList para validar que todo el pipeline funcione correctamente
_Validaciones.
_Orquestacion.
_Limpieza de Espacios en blanco.
_Funcion para borrar archivos descargados
_Monitoreo de Logging
_Principios ACID
_Validar que las rutas funcionen en linux
_Logs de insersión


Pendientes para luego:
_Validar que la actualizacion de las columnas timestamp sea correcta
_Colocar update_at en general sales

1. El Objetivo Principal: Consolidar y Evaluar Órdenes 📊
"Necesitamos un sistema que lea la información de varios reportes diarios y la junte en un solo archivo maestro, limpio y actualizado. El objetivo final es poder saber el estado real de cada orden, cuánto dinero ha entrado, y verificar si la liquidación (el pago final) fue correcta, especialmente las órdenes entregadas y devueltas."

2. Preparar y Actualizar los Reportes Históricos (Funciones get_current_data y update_excel_file_pandas)
"Antes de juntar todo, tenemos que asegurarnos de que los archivos de trabajo (como el Historial de Cartera) estén completos y actualizados.

Paso 1: Encontrar los Archivos Nuevos: Debemos buscar los reportes más recientes (por ejemplo, el último reporte de Órdenes o de Historial de Cartera) en nuestra carpeta. Si es un reporte que se complementa (como el de Historial), hay que juntar los dos archivos más recientes para tener la información completa.

Paso 2: Actualizar el Archivo Histórico: El archivo que guarda el Historial de Cartera es acumulativo. Hay que tomar el reporte nuevo que acabamos de encontrar y usarlo para reemplazar y actualizar la parte vieja del Historial Histórico. Debemos asegurarnos de no duplicar información; solo nos quedamos con la parte del archivo histórico que es más antigua que la fecha inicial del nuevo reporte."

3. Construir la Base de Datos Final (Función merge_Final_dataframes)
"Esta es la parte donde se junta toda la información de las órdenes, garantías, pagos y devoluciones:

Paso A: Iniciar con las Órdenes: Tomamos la lista de órdenes como el punto de partida. Hay que estandarizar el nombre de los estados de la orden (por ejemplo, 'Completada' y 'Finalizada' deben llamarse igual, digamos, 'ENTREGADO').

Paso B: Añadir las Garantías: Para cada orden que tiene garantía, hay que agrupar todos los códigos de garantía asociados a ella y ponerlos en una sola celda.

Paso C: Añadir el Historial de Pagos:

Hay que identificar la fecha más reciente en la que se registró un pago para esa orden.

Debemos calcular el monto total pagado para la orden. Si en el historial aparece un movimiento como 'Salida' (un descuento o devolución), debe restarse; si es una 'Entrada', debe sumarse.

Paso D: Añadir las Devoluciones: Si la orden se devolvió, hay que traer la fecha y el ID del registro de devolución.

Paso E: El Chequeo de Verificación (Liquidación): Aplicamos una lógica de negocio para ver si la orden está 'limpia':

Si el estado final es 'ENTREGADO', comparamos el monto que nos debían pagar versus el monto que calculamos que se pagó. Si coinciden, está 'OK'. Si no, está 'A REVISAR'.

Si el estado es 'DEVUELTO', revisamos si tiene una fecha de devolución asociada. Si la tiene, está 'OK'; si no, está 'A REVISAR' (posiblemente la devolución está incompleta)."

4. Mantener la Base Maestra (Función actualizar_data_dropi)
"Una vez que tenemos la información nueva y consolidada (df_base), hay que usarla para actualizar nuestro archivo maestro final (df_dropi) de esta manera:

Añadir lo Nuevo: Cualquier orden nueva que aparezca en la información consolidada debe añadirse al archivo maestro.

Actualizar lo Existente: Para las órdenes que ya existen en el maestro:

Debemos actualizar cualquier dato que haya cambiado (dirección, monto, etc.).

Manejar el Historial de Estados: Si el estado de la orden ha cambiado (por ejemplo, de 'En Tránsito' a 'Entregado'), el nuevo estado debe añadirse al final de una columna que guarda un historial de todos los estados que ha tenido la orden, y la fecha de hoy debe registrarse como la fecha de ese último cambio."

Perfecto ✅ — ya analicé tu archivo `data_processing.py`, y puedo explicarte claramente la **lógica de cada una de las columnas** que mencionas (y algunas adicionales que también tienen tratamiento especial).

Aquí va el resumen detallado:

---

### 🧩 **Columnas y su lógica**

#### 1. **ESTATUS (TODOS LOS STATUS)**

* Se genera en la función `actualizar_data_dropi`.
* Guarda **el historial acumulado de todos los estatus** que una orden ha tenido.
* Cada vez que cambia el `ULTIMO STATUS`, se concatena el nuevo valor a la cadena existente (separado por coma).

📘 Ejemplo:

```
ANTES: "PENDIENTE"
NUEVO ESTATUS: "EN TRANSITO"
→ TODOS LOS STATUS: "PENDIENTE, EN TRANSITO"
```

---

#### 2. **ULTIMO ESTATUS**

* En `merge_Final_dataframes`, se toma la columna original `ESTATUS` de las órdenes.
* Se renombra a `ULTIMO STATUS`.
* Luego se **mapea** con la función `mapear_status`, que traduce los estados originales a una categoría más estandarizada.

📘 Ejemplo de mapeo:

```
"DEVOLUCION A REMITENTE" → "EN DEVOLUCION"
"EN REPARTO" → "EN TRANSITO"
"ENTREGADO" → "ENTREGADO"
```

---

#### 3. **FECHA ULTIMO ESTATUS**

* Se actualiza en `actualizar_data_dropi`.
* Se guarda la **fecha actual (día del cambio)** cuando el `ULTIMO STATUS` cambia respecto al valor anterior.

📘 Ejemplo:

```
Si hoy = 30/10/2025 y cambia el status → FECHA ULTIMO STATUS = "30/10/2025"
```

---

#### 4. **TOTAL DE LA ORDEN (ÚLTIMA)**

* Entra directamente desde el archivo de órdenes (`df_ordenes`).
* No se transforma dentro del código, solo se conserva tal cual.

---

#### 5. **TIENDA (DROP)**

* También proviene directamente de `df_ordenes` (columna `TIENDA`).
* En el proceso de actualización con `actualizar_data_dropi`, solo se sobrescribe si cambia respecto al valor previo.

---

#### 6. **GARANTIAS**

* Se genera a partir de `df_garantias`.
* Agrupa los registros por `wGarantiaID` y concatena todos los `ID GARANTIA` relacionados.
* Luego se hace un **merge** con el dataframe base.

📘 Ejemplo:

```
wGarantiaID = G001 → IDs: [101, 102]
→ GARANTIAS = "101, 102"
```

---

#### 7. **FECHA ENTRADA DINERO (HISTORIAL) - ULTIMA**

* Calculada desde `df_historial`.
* Se agrupan las transacciones por `NUMERO DE GUIA` y se toma la **fecha máxima (`max`)**.
* Representa la **última fecha en la que entró dinero**.

📘 Ejemplo:

```
Guía X → fechas [2024-08-01, 2024-08-03]
→ FECHA ULTIMA ENTRADA DINERO = 2024-08-03
```

---

#### 8. **MONTO PAGADO ORDEN (SUMA O RESTA)**

* Se basa también en `df_historial`.
* Multiplica el `MONTO` por:

  * `+1` si `TIPO` = "ENTRADA"
  * `-1` si `TIPO` = "SALIDA"
* Luego suma todos los resultados por número de guía.
* Resultado = total neto de pagos (entradas - salidas).

📘 Ejemplo:

```
ENTRADA 1000, SALIDA 200 → MONTO PAGADO ORDEN = 800
```

---

#### 9. **VERIFICACION**

* Se calcula fila por fila según el estatus y el monto pagado:

  * Si `ULTIMO STATUS = ENTREGADO` y `PRECIO PROVEEDOR X CANTIDAD == MONTO PAGADO ORDEN` → **"OK"**
  * Si `ULTIMO STATUS = ENTREGADO` y los montos no coinciden → **"POR REVISAR"**
  * Si `ULTIMO STATUS` es `EN TRANSITO` o `EN DEVOLUCION` → **"PENDIENTE"**
  * Si `ULTIMO STATUS = DEVUELTO` y tiene `FECHA DEVOLUCION` → **"OK"**, si no → **"POR REVISAR"**
  * En cualquier otro caso → **"SIN DEFINIR"**

---

#### 10. **VERIFICACION DE MONTO**

* ⚠️ Esta columna **no está implementada explícitamente** en el código actual.
* Probablemente era una versión previa o un cálculo redundante respecto a `VERIFICACION`.
* Podría implementarse comparando el monto pagado con el total esperado, si lo deseas.

---

#### 11. **FECHA DEVOLUCION**

* Proviene de `df_devoluciones`.
* Se une por `wDevolucionesID` y representa la **fecha en que se registró la devolución**.

---

#### 12. **NUMERO ID**

* También viene de `df_devoluciones`, columna `ID`.
* Es el identificador asociado a la devolución.

---

#### 13. **DEVOLUCIONES**

* Mencionada en tu lista pero no implementada aún.
* Se ve el campo `wDevolucionesID` como enlace, pero no se genera una columna que liste devoluciones (similar a “GARANTIAS”).
* Posiblemente planeabas crear algo como:

  ```python
  df_devoluciones.groupby('wDevolucionesID')['ID'].apply(', '.join)
  ```

---

### ⚙️ Otras columnas con tratamiento especial

| Columna                         | Lógica                                                                    |
| ------------------------------- | ------------------------------------------------------------------------- |
| **UniqueID**                    | Se genera combinando varias columnas clave con `create_unique_id_column`. |
| **COSTO DEL PRODUCTO**          | Se crea vacía (por completar en el futuro).                               |
| **FECHA GUIA GENERADA**         | Se hereda directamente del Excel base.                                    |
| **PRECIO PROVEEDOR X CANTIDAD** | Usada para la verificación de montos.                                     |

---

¿Quieres que te genere un **diagrama de flujo** o **resumen visual** de cómo se construye cada una dentro del proceso (desde qué dataframe y en qué paso)?
Eso te ayudaría mucho si estás rehaciendo la lógica o modularizando el código.
