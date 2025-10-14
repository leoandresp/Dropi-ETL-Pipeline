Realizar CheckList para validar que todo el pipeline funcione correctamente
Ordenes: Se actualizan
Garantias: Se sustituyen
Historial Cartera: Se actualiza
Devoluciones: Se actualizan

Tengo entendido que, las ordenes se pueden repetir por dia, segun cambie de 
status.

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