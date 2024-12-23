import sqlite3

def init_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    
    #tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    #tabla de transferencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            dni TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            date TEXT NOT NULL,
            product_code TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL
        )
    ''')

    #tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT NOT NULL,
            title TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total_price REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_product(code, title, author, stock, price):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (code, title, author, stock, price) VALUES (?, ?, ?, ?, ?)', 
                   (code, title, author, stock, price))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def delete_product(product_id):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

def add_transfer(client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transfers (client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price))
    conn.commit()
    conn.close()

def get_transfers():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transfers')
    transfers = cursor.fetchall()
    conn.close()
    return transfers

def update_transfer(transfer_id, client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE transfers SET client_name = ?, dni = ?, phone = ?, email = ?, payment_method = ?, date = ?, product_code = ?, quantity = ?, total_price = ? WHERE id = ?', 
                   (client_name, dni, phone, email, payment_method, date, product_code, quantity, total_price, transfer_id))
    conn.commit()
    conn.close()

def get_transfer(transfer_id):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transfers WHERE id = ?', (transfer_id,))
    transfer = cursor.fetchone()
    conn.close()
    return transfer

def delete_transfer(transfer_id):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transfers WHERE id = ?', (transfer_id,))
    conn.commit()
    conn.close()

def update_product(product_id, code, title, author, stock, price):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET code = ?, title = ?, author = ?, stock = ?, price = ? WHERE id = ?', 
                   (code, title, author, stock, price, product_id))
    conn.commit()
    conn.close()

def get_product(product_id):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def add_sale(product_code, title, quantity, price, total_price):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sales (product_code, title, quantity, price, total_price) VALUES (?, ?, ?, ?, ?)', 
                   (product_code, title, quantity, price, total_price))
    conn.commit()
    conn.close()

def get_sales():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales')
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_total_sales():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_price) FROM sales')
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0