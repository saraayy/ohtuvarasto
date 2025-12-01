from varasto import Varasto


class WarehouseManager:
    """Manages multiple warehouses, each containing multiple items."""
    
    def __init__(self):
        self.warehouses = {}
        self.next_id = 1
    
    def create_warehouse(self, name, capacity=1000.0):
        """Create a new warehouse with a given name and capacity."""
        warehouse_id = self.next_id
        self.next_id += 1
        self.warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'capacity': capacity,
            'items': {}
        }
        return warehouse_id
    
    def get_warehouse(self, warehouse_id):
        """Get warehouse by ID."""
        return self.warehouses.get(warehouse_id)
    
    def get_all_warehouses(self):
        """Get all warehouses."""
        return list(self.warehouses.values())
    
    def update_warehouse_name(self, warehouse_id, new_name):
        """Update warehouse name."""
        if warehouse_id in self.warehouses:
            self.warehouses[warehouse_id]['name'] = new_name
            return True
        return False
    
    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse."""
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]
            return True
        return False
    
    def add_item(self, warehouse_id, item_name, quantity):
        """Add an item to a warehouse or increase its quantity."""
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse:
            return False
        
        items = warehouse['items']
        if item_name not in items:
            # Create new Varasto for this item
            items[item_name] = Varasto(warehouse['capacity'])
        
        # Add to the warehouse
        items[item_name].lisaa_varastoon(quantity)
        return True
    
    def remove_item(self, warehouse_id, item_name, quantity):
        """Remove quantity from an item in a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse or item_name not in warehouse['items']:
            return False
        
        varasto = warehouse['items'][item_name]
        removed = varasto.ota_varastosta(quantity)
        
        # If the item is now empty, remove it completely
        if varasto.saldo == 0:
            del warehouse['items'][item_name]
        
        return removed
    
    def delete_item(self, warehouse_id, item_name):
        """Delete an item completely from a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse or item_name not in warehouse['items']:
            return False
        
        del warehouse['items'][item_name]
        return True
    
    def get_item_quantity(self, warehouse_id, item_name):
        """Get the current quantity of an item in a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse or item_name not in warehouse['items']:
            return 0
        
        return warehouse['items'][item_name].saldo
    
    def get_warehouse_utilization(self, warehouse_id):
        """Get the total utilization across all items in a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse:
            return 0
        
        total = sum(varasto.saldo for varasto in warehouse['items'].values())
        return total
