import requests
from flask import Flask, render_template, request, jsonify, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Database setup
def setup_database():
    try:
        sqlite_connection = sqlite3.connect("sql_python.db")
        cursor = sqlite_connection.cursor()
        print("Connection successful")

        # Create pizzas_list table
        create_table_query = '''CREATE TABLE IF NOT EXISTS pizzas_list (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            ingredients TEXT NOT NULL,
            image BLOB NOT NULL
        );'''
        cursor.execute(create_table_query)

        # Create orders table
        create_orders_table_query = '''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pizza_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            address TEXT NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
        cursor.execute(create_orders_table_query)

        # Insert initial data into pizzas_list
        insert_query = '''INSERT OR IGNORE INTO pizzas_list (id, name, price, ingredients, image)
        VALUES (1, "Одне сало", 170, "Смалець, сало свиняче копчене, бекон", 
        "https://files.oaiusercontent.com/file-4LZ9LEt60GY3ADcqeGgnskHU");'''
        cursor.execute(insert_query)

        insert_query = '''INSERT OR IGNORE INTO pizzas_list (id, name, price, ingredients, image)
        VALUES (2, "Тисяча градусів за цельсієм", 220, "Соус Табаско, чорізо, сир пекорино, перець халапеньйо", 
        "https://files.oaiusercontent.com/file-yridI9zuglCgwKKlpj3Ax1AT");'''
        cursor.execute(insert_query)

        insert_query = '''INSERT OR IGNORE INTO pizzas_list (id, name, price, ingredients, image)
        VALUES (3, "Чотири соуси", 135, "Соус томатний, соус мексиканьский, соус американьский, чосниковий соус", 
        "https://files.oaiusercontent.com/file-JDYl26QAJCRWU8bdw13GqnCR");'''
        cursor.execute(insert_query)

        sqlite_connection.commit()
        print("Initial data inserted")

    except sqlite3.Error as error:
        print("Error connecting to DB:", error)

    finally:
        if cursor:
            cursor.close()
        if sqlite_connection:
            sqlite_connection.close()
            print("Connection with SQL closed")

setup_database()

# Flask routes
@app.get("/")
def first_page():
    location = "Warsaw"
    weather_data = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=c5a15a87cf2ee0765b0ec6ce5bc3b372&units=metric"
    ).json()

    weather = {
        "temp": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
    }

    return render_template(
        "firstpage.html",
        title="Oderman",
        weather=weather,
        order="Замовлення",
        news="Новини",
        menu_pizza="Меню піццерії",
    )

@app.get("/menu/")
def menu_list():
    pizzas = get_all_pizzas()
    return render_template("menu.html", menu="Меню", our_pizza="Наша піцца", order="Замовлення", news="Новини", menu_pizza="Меню піццерії", pizzas=pizzas)

@app.get("/order/")
def orders():
    return render_template("order.html")

@app.post("/order/")
def place_order():
    pizza_name = request.form["pizza_name"]
    quantity = request.form["quantity"]
    customer_name = request.form["customer_name"]
    address = request.form["address"]

    # Save the order to the database
    save_order(pizza_name, quantity, customer_name, address)

    # Flash a success message
    flash(f"Ваше замовлення на {quantity} піц {pizza_name} успішно оформлено!", "success")

    return render_template("order.html")

def get_all_pizzas():
    sqlite_connection = sqlite3.connect("sql_python.db")
    cursor = sqlite_connection.cursor()
    try:
        cursor.execute("SELECT * FROM pizzas_list")
        pizzas = cursor.fetchall()
        return [{"id": row[0], "name": row[1], "price": row[2], "ingredients": row[3], "image": row[4]} for row in pizzas]
    finally:
        cursor.close()
        sqlite_connection.close()

def save_order(pizza_name, quantity, customer_name, address):
    try:
        sqlite_connection = sqlite3.connect("sql_python.db")
        cursor = sqlite_connection.cursor()
        sqlite_insert_with_param = """INSERT INTO orders (pizza_name, quantity, customer_name, address)
                                      VALUES (?, ?, ?, ?);"""
        data_tuple = (pizza_name, quantity, customer_name, address)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Error while inserting order:", error)
    finally:
        if cursor:
            cursor.close()
        if sqlite_connection:
            sqlite_connection.close()

@app.get("/new_pizza/")
def get_new_pizza_form():
    return render_template("new_pizza.html")

@app.post("/new_pizza/")
def post_new_pizza():
    id = request.form["id"]
    name = request.form["name"]
    price = request.form["price"]
    ingredients = request.form["ingredients"]
    image = request.form["image"]
    save_to_db(id, name, price, ingredients, image)
    pizzas = get_all_pizzas()
    return render_template("menu.html", pizzas=pizzas)

def save_to_db(id, name, price, ingredients, image):
    try:
        sqlite_connection = sqlite3.connect("sql_python.db")
        cursor = sqlite_connection.cursor()
        print("Підключення успішне")

        sqlite_insert_with_param = """INSERT INTO pizzas_list (id, name, price, ingredients, image)
                                      VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (id, name, price, ingredients, image)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Запис додано")
    except sqlite3.Error as error:
        print("Error connecting to DB:", error)
    finally:
        if cursor:
            cursor.close()
        if sqlite_connection:
            sqlite_connection.close()

if __name__ == '__main__':
    app.run(port=5051, debug=True)