from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

pizzas = [
    {"name": "Одне Сало", "price": 170, "ingredients": "Смалець, сало свиняче копчене, бекон", "image_url": "https://tashirpizza.ru/images/products/44-1374.png"},
    {"name": "Тисяча градусів за цельсієм", "price": 220, "ingredients": "Соус Табаско, чорізо, сир пекорино, перець халапеньйо", "image_url": "https://i0.wp.com/www.izumi-sushi.kz/wp-content/uploads/D181D0B0D0BBD18FD0BCD0B8.webp?fit=300%2C300&ssl=1"},
    {"name": "Чотири соуси", "price": 135, "ingredients": "Соус томатний, соус мексиканьский, соус американьский, чосниковий соус", "image_url": "https://sergiopizza.ru/upload/iblock/4f4/4f4b7fa79e8465500baa585cf4f8b803.png"}
]

@app.get("/")
def first_page():
    return render_template("firstpage.html", title="Три ківбаски", order="Замовлення", news="Новини", menu_pizza="Меню піццерії")

@app.get("/menu/")
def menu_list():
    return render_template("menu.html", menu="Меню", our_pizza="Наша піцца", pizzas=pizzas)

@app.get("/order/")
def orders():
    return render_template()

try:
    sqlite_connection = sqlite3.connect("sql_python.db")

    cursor = sqlite_connection.cursor()
    print("Connection succesfull")

    create_table_query = '''CREATE TABLE IF NOT EXISTS pizzas_list (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL ,
    ingredients TEXT NOT NULL,
    image BLOB NOT NULL
    );
    '''
    cursor.execute(create_table_query)

    insert_query = '''INSERT INTO pizzas_list (id, name, price, ingredients, image)
    VALUES (1, "Одне сало", "170", "Смалець, сало свиняче копчене, бекон", "https://tashirpizza.ru/images/products/44-1374.png")'''
    cursor.execute(insert_query)

    insert_query = '''INSERT INTO  pizzas_list (id, name, price, ingredients, image)
    VALUES (2, "Тисяча градусів за цельсієм", "220", "Соус Табаско, чорізо, сир пекорино, перець халапеньйо", "https://i0.wp.com/www.izumi-sushi.kz/wp-content/uploads/D181D0B0D0BBD18FD0BCD0B8.webp?fit=300%2C300&ssl=1")'''
    cursor.execute(insert_query)

    insert_query = '''INSERT INTO  pizzas_list (id, name, price, ingredients, image)
        VALUES (3, "Чотири соуси", "135", "Соус томатний, соус мексиканьский, соус американьский, чосниковий соус", "https://sergiopizza.ru/upload/iblock/4f4/4f4b7fa79e8465500baa585cf4f8b803.png")'''
    cursor.execute(insert_query)

    sqlite_connection.commit()
    cursor.close()


    sqlite_select_query = "SELECT sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("SQL Version", record)
    cursor.close()
except sqlite3.Error as error:
    print("Error conect to DB", error)

finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Connection with SQL closed")


def save_to_db(id, name, email, joing_date, salary):
    try:
        sqlite_connection = sqlite3.connect("sql_python.db")

        cursor = sqlite_connection.cursor()
        print("Підключення успішне")

        sqlite_insert_with_param = """INSERT INTO db_developers
                                          (id, name, price, ingredients, image)
                                          VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (id, name, email, joing_date, salary)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Запис додано")


    except sqlite3.Error as error:
        print("Error conect to DB", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Connection with SQL closed")


@app.get("/new_pizza/")
def get_join():
    return render_template("new_pizza.html")
@app.post("/new_pizza/")
def post_join():
    id = request.form["id"]
    name = request.form["name"]
    price = request.form["price"]
    ingredients = request.form["ingredients"]
    image = request.form["image"]
    save_to_db(id, name, price, ingredients, image)
    return render_template("menu.html")

if __name__ == '__main__':
    app.run(port=5051, debug=True)


