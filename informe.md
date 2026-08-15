# Informe tecnico: Procesamiento concurrente de pedidos con hilos - NovaTech

## Introduccion

En esta tarea se desarrollo una aplicacion de consola en Python para simular una tienda tecnologica llamada NovaTech. El problema consiste en procesar varios pedidos al mismo tiempo usando hilos reales. Cada pedido puede aprobarse, rechazarse por falta de stock o marcarse como error si tiene datos invalidos.

La idea principal fue representar una situacion comun: una tienda tiene un inventario limitado y varios pedidos llegan para ser atendidos. Si varios trabajadores revisan y modifican el inventario sin control, puede ocurrir una condicion de carrera. Por eso el programa usa una cola compartida para repartir los pedidos y un bloqueo para proteger el inventario.

## Implementacion

El programa esta en `main.py`. Primero se carga un inventario inicial con cinco productos: teclado mecanico, mouse inalambrico, audifonos USB, camara web y monitor de 24 pulgadas. Despues se cargan 20 pedidos de prueba. Algunos pedidos son normales, otros compiten por las ultimas unidades de un producto, otros piden mas unidades de las disponibles y otros tienen datos invalidos.

La cola de pedidos se implemento con `Queue`. El hilo principal carga todos los pedidos en esa cola y luego crea tres trabajadores: `WORKER-1`, `WORKER-2` y `WORKER-3`. Cada trabajador retira pedidos de la cola, muestra cuando inicia el pedido, espera entre 0.5 y 2 segundos para simular trabajo y despues valida el inventario.

Tambien se agrego un hilo monitor. Este hilo imprime periodicamente cuantos pedidos quedan pendientes, cuantos fueron aprobados, cuantos rechazados, cuantos fallaron y cuantos trabajadores siguen activos. El monitor no procesa pedidos; solo observa el estado del programa mientras los trabajadores trabajan.

## Condicion de carrera

Una condicion de carrera podria ocurrir si dos trabajadores revisan el inventario al mismo tiempo sin sincronizacion. Por ejemplo, si quedan 2 monitores y dos trabajadores leen ese mismo valor, ambos podrian creer que pueden vender 2 unidades. Si los dos descuentan despues, el sistema terminaria vendiendo mas producto del disponible.

Ese error es peligroso porque el inventario podria quedar negativo o mostrar datos que no corresponden con los pedidos realmente aprobados. En una tienda real esto seria un problema porque se aceptarian pedidos que no se pueden entregar.

## Seccion critica

Para evitar ese problema se uso `Lock`. La comprobacion de existencia, la revision de cantidad disponible y el descuento del inventario se hacen dentro de la misma seccion critica.

La pausa artificial del trabajador ocurre antes de entrar al `Lock`. Esto es importante porque no conviene bloquear el inventario mientras un trabajador solo esta simulando trabajo. El bloqueo se usa solo durante la parte realmente compartida: revisar y modificar el stock.

## Evitar pedidos duplicados

Para repartir los pedidos se uso `Queue`. Cada pedido entra una vez a la cola y cada trabajador retira un pedido con `get_nowait()`. Cuando un trabajador toma un pedido, ese pedido ya no queda disponible para los demas. Asi se evita que dos hilos procesen el mismo pedido.

Al terminar cada pedido se llama `task_done()`. Esto ayuda a mantener la cola en un estado correcto y deja claro que el pedido retirado ya fue atendido.

## Finalizacion del monitor

El monitor se controla con un `Event`. Mientras el evento no esta activado, el monitor sigue mostrando informacion cada segundo. Cuando los trabajadores terminan, el hilo principal activa el evento con `monitorStopEvent.set()` y despues espera al monitor con `monitor.join()`.

Con esto el monitor no queda ejecutandose despues de que el trabajo principal ya termino. En el resumen final tambien se muestra que los hilos de la aplicacion activos son 0.

## Rendimiento

Se hicieron dos pruebas reales desde la consola. En una ejecucion normal con 3 trabajadores, el programa proceso los 20 pedidos en 9.61 segundos. Luego se hizo una prueba temporal con 1 trabajador usando el mismo conjunto de pedidos y el tiempo fue de 24.80 segundos.

La diferencia se debe a que con 3 trabajadores varios pedidos se atienden al mismo tiempo. Como cada pedido tiene una espera simulada entre 0.5 y 2 segundos, usar varios hilos reduce el tiempo total. Con 1 trabajador, los pedidos se atienden uno por uno y el tiempo se acumula mas.

Los tiempos pueden variar un poco en cada ejecucion porque las pausas son aleatorias, pero la comparacion muestra claramente que la concurrencia mejora el tiempo total para este tipo de simulacion.

## Resultados de los casos de prueba

En CP-01 se observa el flujo normal. Varios pedidos aparecen como `APROBADO` y los mensajes de `WORKER-1`, `WORKER-2` y `WORKER-3` se intercalan, lo que demuestra que los hilos trabajan al mismo tiempo.

En CP-02 se observa la contencion. Varios pedidos usan productos limitados como `P005` y `P002`. Algunos pedidos son aprobados, pero cuando ya no queda suficiente inventario, otros son rechazados por stock insuficiente. El inventario final no queda negativo.

En CP-03 se valida el stock insuficiente. El pedido `ORD-016` solicita 10 unidades de `P001`, pero para ese momento no hay suficientes unidades disponibles. El pedido se rechaza sin descontar inventario.

En CP-04 se revisan pedidos invalidos. Los pedidos con producto inexistente, cantidad cero, cantidad negativa o estructura incompleta se registran como `ERROR`. Estos errores no detienen a los trabajadores ni al resto del procesamiento.

En CP-05 se comprueba el cierre limpio. Al final aparecen los `join` completados, el monitor detenido correctamente, pedidos pendientes en 0 y hilos activos de la aplicacion en 0.

## Conclusion

La tarea muestra como usar hilos para procesar trabajo de forma concurrente y como proteger recursos compartidos. La `Queue` sirvio para repartir pedidos sin duplicarlos, el `Lock` evito errores en el inventario y el `Event` permitio detener el monitor de manera controlada.

El resultado final cumple con el escenario de NovaTech: hay procesamiento concurrente real, sincronizacion del inventario, manejo de errores, resumen final y cierre limpio de los hilos.
