# Préstamo de equipo

Mauricio Maradiaga  
Cuenta 0801200605500  
Programación de Negocios · Odoo 20

## Respuestas

### Paso 1. Catálogo de equipos

**1. ¿Qué pasa con un equipo cuando se desmarca el campo Activo? ¿Por qué es mejor que borrarlo?**

Si le quito la marca de Activo a una laptop, Odoo la archiva y deja de salir en la lista que veo normalmente. Me conviene archivarla porque puede que esa laptop ya se haya prestado varias veces. Así, si después ocupo revisar uno de esos préstamos, todavía puedo ver qué equipo era. También la puedo volver a activar.

**2. ¿Para qué sirve `copy=False` en el campo `codigo`?**

Sirve para que el código de inventario quede vacío cuando duplico un equipo. Por ejemplo, si uso la Laptop Dell 01 como base para registrar otra igual, puedo aprovechar su nombre y categoría, pero tengo que escribir el código que le corresponde a la nueva.

### Paso 2. Registro de préstamos

**1. Este modelo usa `_name` y `_inherit` al mismo tiempo. ¿Qué hace cada uno aquí?**

Con `_name` le pongo al modelo de préstamos el nombre `prestamo.prestamo`. Con `_inherit` aprovecho lo que ya trae `mail.thread` para manejar mensajes y guardar cambios. Así, cuando abro un préstamo, ahí mismo puedo leer lo que ha pasado con él.

**2. ¿Qué hace `tracking=True` en el campo `state`?**

Hace que el cambio de estado quede anotado en el historial del préstamo. Por ejemplo, cuando le doy a Prestar, puedo ver que antes estaba en Borrador y que pasó a Prestado. Si después alguien lo devuelve, también queda registrado ese cambio.

### Paso 3. Equipos del préstamo

**1. En `fields.One2many("prestamo.linea", "prestamo_id")`, ¿qué indica cada parámetro?**

El primero, `prestamo.linea`, indica dónde se guarda cada línea de equipo. El segundo, `prestamo_id`, le dice a Odoo qué campo de esa línea debe revisar para saber a qué préstamo pertenece. Si agrego una laptop y un proyector al mismo préstamo, quedan dos líneas con el mismo `prestamo_id`. Por eso me salen juntas cuando abro el formulario.

**2. ¿Qué pasa con las líneas cuando se borra un préstamo? ¿Qué parte del código lo define?**

Al borrar el préstamo también se borran las líneas que le pertenecen. Eso lo define `ondelete="cascade"` en el campo `prestamo_id`. En el ejemplo de la laptop y el proyector, se borran los dos renglones de ese préstamo y los equipos siguen en el catálogo.

### Paso 4. Flujo de estados

**1. Los botones ya se ocultan según el estado. ¿Por qué los métodos vuelven a validar el estado?**

Puede pasar que dos personas tengan abierto el mismo préstamo en Borrador. Si una ya entregó el equipo, la otra todavía podría tener el botón Prestar en su pantalla. Por eso, cuando le da al botón, el método revisa cómo está el préstamo en ese momento. Si ya aparece como Prestado, Odoo detiene la segunda entrega.

**2. ¿Qué hace `prestamo.linea_ids.equipo_id.write(...)`? ¿Por qué no hace falta un `for` para cada equipo?**

`linea_ids` me da las líneas del préstamo y con `equipo_id` obtengo los equipos de esas líneas. Odoo permite usar `write` sobre todo ese grupo de una vez. Si el préstamo lleva una laptop y un proyector, con la misma llamada los dos pasan a Prestado. Al devolverlos se hace lo mismo para dejarlos disponibles.

### Paso 5. Reglas del préstamo

**1. El campo `equipo_id` ya filtra los equipos disponibles. ¿Por qué hace falta el TODO 5?**

Porque el equipo puede cambiar de estado entre el momento en que lo elijo y el momento en que lo entrego. Yo puedo dejar una laptop en un borrador y que después alguien la mande a mantenimiento. Al darle a Prestar, el sistema revisa otra vez y me dice cuál equipo ya no está disponible.

**2. ¿En qué momento se ejecuta un método con `@api.constrains`? ¿Y la validación de `action_prestar`?**

Odoo revisa `@api.constrains` cuando creo o actualizo el registro con alguno de los campos que aparecen en esa regla. Por ejemplo, si pongo la devolución antes del día del préstamo, el error me sale al guardar. En cambio, la validación de `action_prestar` se hace cuando le doy a Prestar. Ahí es donde se comprueba, entre otras cosas, si un estudiante está intentando llevar más de dos equipos.

### Paso 6. Contacto, kanban y búsqueda

**1. ¿Qué pasa si arrastra una tarjeta del kanban a otra columna? ¿Por qué?**

Si paso una laptop de Disponible a En mantenimiento, Odoo guarda En mantenimiento como su nuevo estado. Eso pasa porque las columnas están agrupadas por el campo `estado`. El cambio también se ve al abrir la ficha de la laptop. Si ya está prestada, la regla de mantenimiento me pide devolverla primero.

**2. El campo `prestamo_ids` se agregó a `res.partner`. ¿Se crea una columna nueva en la tabla de contactos? Explique.**

No se crea otra columna en contactos. Cada préstamo ya guarda quién lo pidió en el campo `partner_id`. Cuando abro la pestaña Préstamos de un contacto, Odoo busca los préstamos que tienen a esa persona como solicitante y me los muestra ahí. Así puedo revisar todo lo que ha pedido desde su ficha.
