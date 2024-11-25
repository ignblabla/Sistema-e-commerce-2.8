# Sistema E-Commerce EDB 2.8

# Product Backlog para el Sistema e-Commerce

![Imagen del Proyecto](https://www.informatica.us.es/docs/imagen-etsii/logo-ETSII-US-Vertical-Color.png)

## Componentes <a name="componentes"></a>

- Ignacio Blanquero Blanco
- Adrián Cabello Martín
- María de la Salud Carrera Talaverón
- Antonio Montero López
- Natalia Olmo Villegas
 
## Tabla de Versiones
| Versión | Fecha       | Descripción                   |
|---------|-------------|-------------------------------|
| 1.0     | 13/11/2024  | Inicialización del documento    |

| **ID**   | **Descripción del Item (PBI)**                                                                               | **Prioridad** | **Criterio de Aceptación**                                                                                   |
|----------|-------------------------------------------------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------------------------------|
| PBI-01   | Visualización constante de la cesta de compra (excepto durante la tramitación).                              | Should Have   | La cesta de compra es visible en todas las pantallas, salvo en las de tramitación, y muestra los elementos actuales. |
| PBI-02   | Función para modificar cantidad de productos en la cesta.                                                    | Must Have     | Botones para aumentar/disminuir cantidades en la cesta que reflejan los cambios aunque se cambie de pantalla. |
| PBI-03   | Organización del catálogo según las categorías de las tiendas físicas.                                       | Should Have   | El catálogo refleja las mismas categorías utilizadas en las tiendas físicas del cliente.                    |
| PBI-04   | Proceso de compra rápida en máximo tres pasos, sin requerir registro.                                        | Should Have   | Usuarios autenticados/no autenticados pueden completar compras en tres pasos con información solicitada según el caso. |
| PBI-05   | Sensación de seguridad en el proceso de compra.                                                              | Must Have     | Feedback positivo del nivel de seguridad por parte de los usuarios en pruebas.                              |
| PBI-06   | Plataforma completamente en español, salvo excepciones aceptadas.                                            | Must Have     | Todo el contenido está en castellano, excepto nombres de productos o términos aprobados por la RAE.         |
| PBI-07   | Identificación por correo electrónico y contraseña.                                                          | Must Have     | Login funcional solo con credenciales válidas (correo y contraseña asociados).                              |
| PBI-08   | Acceso directo al seguimiento de pedidos para usuarios no registrados.                                       | Must Have     | Se muestra información del estado del pedido tras ingresar un identificador válido.                         |
| PBI-09   | Marcado de productos agotados en el catálogo.                                                                | Must Have     | Productos agotados tienen una etiqueta visible; productos disponibles no muestran esta etiqueta.            |
| PBI-10   | Imagen única por producto en el catálogo.                                                                    | Could Have    | Cada producto cuenta con exactamente una imagen asociada.                                                  |
| PBI-11   | Filtrado de catálogo por secciones, departamentos o fabricantes.                                             | Should Have   | Filtros disponibles en el catálogo permiten seleccionar criterios aplicables.                               |
| PBI-12   | Búsqueda en el catálogo por nombre, departamento, sección o fabricante.                                      | Must Have     | Una barra de búsqueda arroja resultados según el nombre o atributos definidos.                              |
| PBI-13   | Barra de búsqueda visible en la página de inicio.                                                            | Should Have   | La barra de búsqueda aparece en la página de inicio y en la de resultados.                                 |
| PBI-14   | Navegación en el catálogo por criterios organizados.                                                         | Should Have   | Botón para ordenar productos según criterios seleccionados o por defecto.                                  |
| PBI-15   | Envío de productos a la cesta desde el catálogo.                                                             | Must Have     | Un botón en el catálogo permite agregar productos a la cesta indicando cantidades.                         |
| PBI-16   | Revisión del estado de la cesta desde el catálogo.                                                           | Must Have     | Visualización del contenido de la cesta y precios desde el catálogo.                                       |
| PBI-17   | Finalización de la compra desde la cesta.                                                                    | Must Have     | Un botón en la cesta permite tramitar el pedido.                                                           |
| PBI-18   | Solicitud de datos del cliente durante el proceso de compra.                                                 | Must Have     | Se solicitan datos automáticamente o manualmente según si el usuario está autenticado.                     |
| PBI-19   | Solicitud de datos de envío durante la compra.                                                               | Must Have     | Los datos de entrega se solicitan antes de finalizar la compra.                                            |
| PBI-20   | Solicitud de datos de pago antes de finalizar la compra.                                                     | Must Have     | Los datos de pago se introducen antes de completar la compra.                                              |
| PBI-21   | Envío de correo de confirmación tras la compra.                                                              | Should Have   | Un correo automático confirma la compra con detalles relevantes.                                           |
| PBI-22   | Exclusión de funciones relacionadas con devoluciones en la tienda online.                                    | Must Have     | No existen funciones de devolución; se indica que deben gestionarse en tiendas físicas.                    |
| PBI-23   | Registro de usuarios mediante correo electrónico y contraseña.                                               | Must Have     | Registro funcional con validación de correo único y contraseña de 8-12 caracteres.                        |
| PBI-24   | Pruebas de la solución disponibles en un PaaS.                                                               | Should Have   | Implementación disponible para pruebas en una plataforma como servicio.                                    |
| PBI-25   | Entrega del producto final como contenedor con instrucciones.                                                | Must Have     | Producto entregado como contenedor con guías de instalación y puesta en producción.                        |
| PBI-26   | Uso de ciclo de vida híbrido para el proyecto.                                                               | Should Have   | El desarrollo sigue un ciclo predictivo para planificación y adaptativo en ejecución.                      |
| PBI-27   | Uso obligatorio de plantillas corporativas.                                                                  | Must Have     | Documentación generada con las plantillas predefinidas por la organización.                                |
