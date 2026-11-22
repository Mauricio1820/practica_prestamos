# Préstamo de equipo

Mauricio Maradiaga  
Cuenta 0801200605500  
Programación de Negocios · Odoo 20

## Respuestas

### Catálogo de equipos

**¿Qué pasa al desmarcar Activo? ¿Por qué conviene archivarlo?**

Al quitar la marca, el equipo queda archivado y desaparece de la lista normal. Si después ocupo ver a quién se prestó, el registro sigue ahí.

**¿Para qué sirve copy=False en el código?**

Si duplico una laptop, Odoo deja vacío el código de inventario para que escriba el del otro equipo.

### Registro de préstamos

**¿Qué hacen _name y _inherit en este modelo?**

Con _name le doy al préstamo su propio modelo, prestamo.prestamo. Con _inherit uso mail.thread para que cada préstamo tenga su historial de mensajes.

**¿Qué hace tracking=True en el estado?**

Cuando cambia el estado, Odoo guarda en el historial el valor anterior y el nuevo. Así puedo ver cuándo pasó de Borrador a Prestado.

### Equipos del préstamo

**¿Qué indican los dos parámetros del One2many?**

prestamo.linea es el modelo donde se guarda cada renglón. prestamo_id es el campo de ese renglón que apunta al préstamo. Así el formulario reúne los equipos que le corresponden.

**¿Qué pasa con las líneas si borro el préstamo?**

Si borro el préstamo, se borran sus líneas por ondelete="cascade" en prestamo_id. Los equipos siguen en el catálogo.

### Entrega y devolución

**¿Por qué se valida el estado si el botón ya está oculto?**

Ocultar el botón solo controla lo que veo en pantalla. Si alguien intenta prestar de nuevo el mismo registro, el método revisa su estado antes de cambiar los equipos.

**¿Cómo se cambia el estado de todos los equipos sin otro ciclo?**

prestamo.linea_ids.equipo_id reúne los equipos de las líneas. Con write cambio el estado de todo ese conjunto en una sola llamada.

### Reglas del préstamo

**¿Por qué revisar la disponibilidad al prestar?**

Puedo elegir una laptop disponible y dejar el préstamo en borrador. Si la pasan a mantenimiento antes de que pulse Prestar, el método tiene que revisar otra vez para impedir la entrega.

**¿Cuándo se ejecutan las restricciones y cuándo se valida el préstamo?**

Odoo ejecuta @api.constrains al crear o modificar un registro con los campos que se revisan. Por eso una fecha incorrecta falla al guardar. El límite de equipos y la disponibilidad se revisan cuando pulso Prestar.
