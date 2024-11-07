import requests
import time

API_URL = "http://127.0.0.1:9420/api/inventory_items/"

def is_inventory_full(inventory):
    return len(inventory) >= 28

def send_inventory_data(inventory):
    response = requests.post(API_URL, json=inventory)
    if response.status_code == 200:
        print(response.json())
    else:
        print("Failed to send inventory data:", response.status_code)

def main():
    inventory = []

    while not is_inventory_full(inventory):
        item = {"name": "ore", "quantity": 1}
        inventory.append(item)
        send_inventory_data(inventory)
        time.sleep(1)

    print("Inventory is full!")

if __name__ == "__main__":
    main() 