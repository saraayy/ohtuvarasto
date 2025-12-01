from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_manager import WarehouseManager

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Create a global warehouse manager
manager = WarehouseManager()


@app.route('/')
def index():
    """Home page showing all warehouses."""
    warehouses = manager.get_all_warehouses()
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        capacity = request.form.get('capacity', '1000')
        
        if not name:
            flash('Warehouse name is required', 'error')
            return render_template('create_warehouse.html')
        
        try:
            capacity = float(capacity)
            if capacity <= 0:
                flash('Capacity must be positive', 'error')
                return render_template('create_warehouse.html')
        except ValueError:
            flash('Invalid capacity value', 'error')
            return render_template('create_warehouse.html')
        
        warehouse_id = manager.create_warehouse(name, capacity)
        flash(f'Warehouse "{name}" created successfully', 'success')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    return render_template('create_warehouse.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View a specific warehouse and its items."""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    utilization = manager.get_warehouse_utilization(warehouse_id)
    return render_template('warehouse.html', warehouse=warehouse, utilization=utilization)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit warehouse name."""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        
        if not new_name:
            flash('Warehouse name is required', 'error')
            return render_template('edit_warehouse.html', warehouse=warehouse)
        
        if manager.update_warehouse_name(warehouse_id, new_name):
            flash(f'Warehouse renamed to "{new_name}"', 'success')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        else:
            flash('Failed to update warehouse', 'error')
    
    return render_template('edit_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if manager.delete_warehouse(warehouse_id):
        flash('Warehouse deleted successfully', 'success')
    else:
        flash('Failed to delete warehouse', 'error')
    
    return redirect(url_for('index'))


@app.route('/warehouse/<int:warehouse_id>/item/add', methods=['POST'])
def add_item(warehouse_id):
    """Add an item to a warehouse."""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    item_name = request.form.get('item_name', '').strip()
    quantity = request.form.get('quantity', '0')
    
    if not item_name:
        flash('Item name is required', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            flash('Quantity must be positive', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid quantity value', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    if manager.add_item(warehouse_id, item_name, quantity):
        flash(f'Added {quantity} of "{item_name}"', 'success')
    else:
        flash('Failed to add item', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/item/<item_name>/increase', methods=['POST'])
def increase_item(warehouse_id, item_name):
    """Increase item quantity."""
    quantity = request.form.get('quantity', '1')
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            flash('Quantity must be positive', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid quantity value', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    if manager.add_item(warehouse_id, item_name, quantity):
        flash(f'Increased "{item_name}" by {quantity}', 'success')
    else:
        flash('Failed to increase item', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/item/<item_name>/decrease', methods=['POST'])
def decrease_item(warehouse_id, item_name):
    """Decrease item quantity."""
    quantity = request.form.get('quantity', '1')
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            flash('Quantity must be positive', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid quantity value', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    removed = manager.remove_item(warehouse_id, item_name, quantity)
    if removed is not False:
        flash(f'Decreased "{item_name}" by {removed}', 'success')
    else:
        flash('Failed to decrease item', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/item/<item_name>/delete', methods=['POST'])
def delete_item(warehouse_id, item_name):
    """Delete an item completely."""
    if manager.delete_item(warehouse_id, item_name):
        flash(f'Deleted "{item_name}"', 'success')
    else:
        flash('Failed to delete item', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    app.run(debug=True)
