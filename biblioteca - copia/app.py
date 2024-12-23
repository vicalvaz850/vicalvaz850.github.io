from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, add_product, get_products, delete_product, add_transfer, get_transfers, update_product, get_product, update_transfer, get_transfer, get_sales, get_total_sales, add_sale

app = Flask(__name__)
app.secret_key = 'secret_key'  # Cambia esto a una clave secreta más segura en producción

#inicia la base de datos
init_db()

#datos de ejemplo
admin_email = "admin@gmail.com"
admin_password = "password123"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']
    if email == admin_email and password == admin_password:
        session['logged_in'] = True
        return redirect(url_for('main'))
    else:
        flash('Credenciales incorrectas')
        return redirect(url_for('login'))

@app.route('/main')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/products')
def products():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    product_list = get_products()
    return render_template('products.html', products=product_list)

@app.route('/add_product', methods=['POST'])
def add_new_product():
    code = request.form['code']
    title = request.form['title']
    author = request.form['author']
    stock = request.form['stock']
    price = request.form['price']
    add_product(code, title, author, stock, price)
    return redirect(url_for('products'))

@app.route('/delete_product/<int:product_id>')
def delete_product_route(product_id):
    delete_product(product_id)
    return redirect(url_for('products'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        code = request.form['code']
        title = request.form['title']
        author = request.form['author']
        stock = request.form['stock']
        price = request.form['price']
        update_product(product_id, code, title, author, stock, price)
        return redirect(url_for('products'))
    
    product = get_product(product_id)
    if product is None:
        flash('Producto no encontrado')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)
    # Aquí deberías obtener el producto de la base de datos
    # (implementa la función get_product en database.py)


@app.route('/transfers')
def transfers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    transfer_list = get_transfers()
    product_list = get_products()  # Obtener productos para el dropdown
    return render_template('transfers.html', transfers=transfer_list, products=product_list)

@app.route('/add_transfer', methods=['POST'])
def add_new_transfer():
    client_name = request.form['client_name']
    dni = request.form['dni']
    phone = request.form['phone']
    email = request.form['email']
    payment_method = request.form['payment_method']
    date = request.form['date']
    product_code = request.form['product_code']
    quantity = request.form['quantity']
    total_price = request.form['total_price']
    add_transfer(client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price)
    return redirect(url_for('transfers'))

@app.route('/edit_transfer/<int:transfer_id>', methods=['GET', 'POST'])
def edit_transfer(transfer_id):
    if request.method == 'POST':
        client_name = request.form['client_name']
        dni = request.form['dni']
        phone = request.form['phone']
        email = request.form['email']
        payment_method = request.form['payment_method']
        date = request.form['date']
        product_code = request.form['product_code']
        quantity = request.form['quantity']
        total_price = request.form['total_price']
        # Aquí deberías implementar la función update_transfer en database.py
        update_transfer(transfer_id, client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price)
        return redirect(url_for('transfers'))
    
    # Aquí deberías obtener la transferencia de la base de datos
    transfer = get_transfer(transfer_id)
    if transfer is None:
        flash('Transferencia no encontrada')
        return redirect(url_for('transfers'))
    
    product_list = get_products()  # Obtener productos para el dropdown
    return render_template('edit_transfer.html', transfer=transfer, products=product_list)

@app.route('/delete_transfer/<int:transfer_id>')
def delete_transfer(transfer_id):
    # Aquí deberías implementar la función delete_transfer en database.py
    delete_transfer(transfer_id)
    return redirect(url_for('transfers'))

@app.route('/sales')
def sales():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    sales_list = get_sales()
    total_sales = get_total_sales()
    transfer_list = get_transfers() # Obtener transferencias para el dropdown
    return render_template('sales.html', sales=sales_list, total_sales=total_sales, transfers=transfer_list)

@app.route('/add_sale', methods=['POST'])
def add_new_sale():
    transfer_id = request.form['transfer_id']
    transfer = get_transfer(transfer_id)  # Obtener la transferencia
    if transfer:
        product_code = transfer[7]  # Suponiendo que el código del producto está en la posición 7
        title = transfer[1]  # Suponiendo que el título está en la posición 1
        quantity = transfer[8]  # Suponiendo que la cantidad está en la posición 8
        price = transfer[9]  # Suponiendo que el precio total está en la posición 9
        total_price = transfer[9]  # Total de la transferencia
        add_sale(product_code, title, quantity, price, total_price)
    return redirect(url_for('sales'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)