from queue import Queue
from threading import Event, Lock, Thread


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


def showInventory(inventory):
    print("\nInventario inicial:")
    for productCode, productData in inventory.items():
        productName = productData["productName"]
        stock = productData["stock"]
        print(f"{productCode} | {productName} | {stock} unidades")


def runApplication():
    print("NovaTech - Procesamiento concurrente de pedidos")
    print("ETAPA 2: inventario cargado correctamente.")
    inventory = createInitialInventory()
    showInventory(inventory)


if __name__ == "__main__":
    runApplication()
