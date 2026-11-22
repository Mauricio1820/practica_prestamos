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
