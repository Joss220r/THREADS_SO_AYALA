from random import uniform
from queue import Empty, Queue
from threading import Event, Lock, Thread
from time import sleep


def createInitialInventory():
    return {
        "P001": {
            "productName": "Teclado mecanico",
            "stock": 12,
        },
        "P002": {
            "productName": "Mouse inalambrico",
            "stock": 18,
        },
        "P003": {
            "productName": "Audifonos USB",
            "stock": 10,
        },
        "P004": {
            "productName": "Camara web",
            "stock": 8,
        },
        "P005": {
            "productName": "Monitor de 24 pulgadas",
            "stock": 6,
        },
    }


def showInventory(inventory, title="Inventario"):
    print(f"\n{title}:")
    for productCode, productData in inventory.items():
        productName = productData["productName"]
        stock = productData["stock"]
        print(f"{productCode} | {productName} | {stock} unidades")


def createOrders():
    return [
        {
            "orderId": "ORD-001",
            "customer": "Ana Lopez",
            "products": [{"productCode": "P001", "quantity": 2}],
        },
        {
            "orderId": "ORD-002",
            "customer": "Carlos Mendez",
            "products": [{"productCode": "P002", "quantity": 3}],
        },
        {
            "orderId": "ORD-003",
            "customer": "Maria Perez",
            "products": [{"productCode": "P003", "quantity": 1}],
        },
        {
            "orderId": "ORD-004",
            "customer": "Jose Garcia",
            "products": [{"productCode": "P004", "quantity": 2}],
        },
        {
            "orderId": "ORD-005",
            "customer": "Lucia Ramos",
            "products": [{"productCode": "P005", "quantity": 1}],
        },
        {
            "orderId": "ORD-006",
            "customer": "Diego Castillo",
            "products": [
                {"productCode": "P001", "quantity": 1},
                {"productCode": "P002", "quantity": 2},
            ],
        },
        {
            "orderId": "ORD-007",
            "customer": "Sofia Herrera",
            "products": [
                {"productCode": "P003", "quantity": 2},
                {"productCode": "P004", "quantity": 1},
            ],
        },
        {
            "orderId": "ORD-008",
            "customer": "Pedro Alvarez",
            "products": [{"productCode": "P005", "quantity": 2}],
        },
        {
            "orderId": "ORD-009",
            "customer": "Elena Torres",
            "products": [{"productCode": "P005", "quantity": 3}],
        },
        {
            "orderId": "ORD-010",
            "customer": "Raul Morales",
            "products": [{"productCode": "P005", "quantity": 2}],
        },
        {
            "orderId": "ORD-011",
            "customer": "Valeria Ruiz",
            "products": [{"productCode": "P002", "quantity": 4}],
        },
        {
            "orderId": "ORD-012",
            "customer": "Andres Molina",
            "products": [{"productCode": "P002", "quantity": 5}],
        },
        {
            "orderId": "ORD-013",
            "customer": "Gabriela Soto",
            "products": [{"productCode": "P002", "quantity": 6}],
        },
        {
            "orderId": "ORD-014",
            "customer": "Hector Diaz",
            "products": [{"productCode": "P003", "quantity": 4}],
        },
        {
            "orderId": "ORD-015",
            "customer": "Natalia Cruz",
            "products": [{"productCode": "P004", "quantity": 3}],
        },
        {
            "orderId": "ORD-016",
            "customer": "Oscar Fuentes",
            "products": [{"productCode": "P001", "quantity": 10}],
        },
        {
            "orderId": "ORD-017",
            "customer": "Patricia Leon",
            "products": [{"productCode": "P999", "quantity": 1}],
        },
        {
            "orderId": "ORD-018",
            "customer": "Roberto Vega",
            "products": [{"productCode": "P003", "quantity": 0}],
        },
        {
            "orderId": "ORD-019",
            "customer": "Camila Reyes",
            "products": [{"productCode": "P004", "quantity": -2}],
        },
        {
            "orderId": "ORD-020",
            "customer": "Fernando Silva",
        },
    ]


def showOrdersSummary(orders):
    print(f"\nPedidos cargados: {len(orders)}")
    for order in orders:
        orderId = order.get("orderId", "SIN-ID")
        customer = order.get("customer", "SIN-CLIENTE")
        products = order.get("products", [])
        print(f"{orderId} | Cliente: {customer} | Productos: {len(products)}")


def loadOrderQueue(orders):
    orderQueue = Queue()
    for order in orders:
        orderQueue.put(order)
    return orderQueue


def processOrderInventory(order, inventory, inventoryLock):
    products = order.get("products")
    if not isinstance(products, list) or len(products) == 0:
        return False, "Pedido sin productos validos"

    with inventoryLock:
        for product in products:
            productCode = product.get("productCode")
            quantity = product.get("quantity")

            if productCode not in inventory:
                return False, f"Producto inexistente {productCode}"

            if not isinstance(quantity, int) or quantity <= 0:
                return False, f"Cantidad invalida {productCode}"

            availableStock = inventory[productCode]["stock"]
            if availableStock < quantity:
                return False, f"Stock insuficiente {productCode}"

        approvedDetails = []
        for product in products:
            productCode = product["productCode"]
            quantity = product["quantity"]
            inventory[productCode]["stock"] -= quantity
            approvedDetails.append(f"{productCode}: -{quantity} unidades")

    return True, ", ".join(approvedDetails)


def hasNegativeStock(inventory):
    return any(productData["stock"] < 0 for productData in inventory.values())


def workerThread(workerName, orderQueue, inventory, inventoryLock):
    while True:
        try:
            order = orderQueue.get_nowait()
        except Empty:
            print(f"[{workerName}] No hay mas pedidos. Trabajador finalizado.")
            break

        orderId = order.get("orderId", "SIN-ID")
        customer = order.get("customer", "SIN-CLIENTE")
        processTime = uniform(0.5, 2.0)

        print(f"[{workerName}] Inicia pedido {orderId} | Cliente: {customer}")
        sleep(processTime)
        isApproved, resultMessage = processOrderInventory(order, inventory, inventoryLock)

        if isApproved:
            print(f"[{workerName}] {orderId} APROBADO | {resultMessage}")
        else:
            print(f"[{workerName}] {orderId} RECHAZADO | {resultMessage}")

        orderQueue.task_done()


def createWorkerThreads(orderQueue, inventory, inventoryLock):
    workerNames = ["WORKER-1", "WORKER-2", "WORKER-3"]
    return [
        Thread(
            target=workerThread,
            name=workerName,
            args=(workerName, orderQueue, inventory, inventoryLock),
        )
        for workerName in workerNames
    ]


def runApplication():
    print("NovaTech - Procesamiento concurrente de pedidos")
    print("ETAPA 7: inventario sincronizado con Lock.")
    inventory = createInitialInventory()
    inventoryLock = Lock()
    orders = createOrders()
    orderQueue = loadOrderQueue(orders)
    workerThreads = createWorkerThreads(orderQueue, inventory, inventoryLock)

    showInventory(inventory, "Inventario inicial")
    showOrdersSummary(orders)

    print("\nIniciando trabajadores:")
    for worker in workerThreads:
        print(f"Se inicia {worker.name}")
        worker.start()

    for worker in workerThreads:
        worker.join()
        print(f"join completado para {worker.name}")

    print(f"Pedidos pendientes al finalizar: {orderQueue.qsize()}")
    showInventory(inventory, "Inventario final temporal")
    print(f"Inventario negativo detectado: {hasNegativeStock(inventory)}")


if __name__ == "__main__":
    runApplication()
