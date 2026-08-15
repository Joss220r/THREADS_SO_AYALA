# NovaTech Threads

Aplicacion de consola en Python para simular el procesamiento concurrente de pedidos de una tienda tecnologica llamada NovaTech.

## Lenguaje y version

- Lenguaje: Python
- Version recomendada: Python 3.10 o superior
- Dependencias externas: ninguna

El programa usa solamente librerias incluidas con Python:

- `threading`
- `Thread`
- `Queue`
- `Lock`
- `Event`
- `join`

## Forma de ejecutar

Desde la carpeta del proyecto:

```powershell
python main.py
```

## Estructura del proyecto

```text
THREADS_SO_AYALA/
|-- main.py
|-- README.md
|-- diagrama.md
|-- informe.md
|-- evidencias/
```

## Estructura de hilos

El programa tiene un hilo principal, tres trabajadores y un monitor.

El hilo principal carga el inventario, carga los pedidos, prepara la cola compartida, crea los recursos sincronizados, inicia los hilos, espera con `join`, detiene el monitor y muestra el resumen final.

Los trabajadores son:

- `WORKER-1`
- `WORKER-2`
- `WORKER-3`

Cada trabajador toma pedidos desde una `Queue`, simula procesamiento con una espera aleatoria entre 0.5 y 2 segundos, valida el pedido, descuenta inventario si corresponde y registra el resultado.

## Queue

La cola compartida se implementa con `Queue`. Cada pedido se carga una sola vez y cada trabajador usa la cola para retirar pedidos pendientes. Esto evita que dos trabajadores procesen el mismo pedido.

## Lock

El inventario se protege con `Lock`. La validacion de stock y el descuento se hacen dentro de la misma seccion critica, para evitar condiciones de carrera y asegurar que el inventario nunca quede negativo.

## Event

El monitor usa un `Event` llamado `monitorStopEvent`. Mientras el evento no esta activado, el monitor imprime el avance del procesamiento. Cuando los trabajadores terminan, el hilo principal activa el evento y el monitor finaliza.

## join

El hilo principal usa `join` para esperar a que terminen los trabajadores y tambien espera al monitor antes de mostrar el resumen final. Esto permite comprobar un cierre limpio.

## Sincronizacion

La pausa artificial del procesamiento ocurre fuera del `Lock`. Solo se bloquea el inventario durante la revision y descuento de productos. Los contadores de resultados tambien se actualizan usando un `Lock` para mantener datos consistentes.

## Casos incluidos

El conjunto de 20 pedidos permite demostrar:

- Flujo normal con pedidos aprobados.
- Contencion por las ultimas unidades de productos como `P005` y `P002`.
- Rechazo por stock insuficiente.
- Pedidos invalidos con producto inexistente, cantidad cero, cantidad negativa o estructura incompleta.
- Cierre limpio con trabajadores, monitor y `join`.
