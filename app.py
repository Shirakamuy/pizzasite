from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
    VALUES (1, "Одне сало", "170", "Смалець, сало свиняче копчене, бекон", "https://files.oaiusercontent.com/file-4LZ9LEt60GY3ADcqeGgnskHU?se=2024-11-14T15%3A55%3A44Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D1e0a7a34-165a-4fc8-8e6a-ac1e712ee0d4.webp&sig=sP%2B1KNfTT2OmtxNWvzCx39QsQshIr/MgJgMEG7X7gtc%3D")'''
    cursor.execute(insert_query)

    insert_query = '''INSERT INTO  pizzas_list (id, name, price, ingredients, image)
    VALUES (2, "Тисяча градусів за цельсієм", "220", "Соус Табаско, чорізо, сир пекорино, перець халапеньйо", "https://files.oaiusercontent.com/file-yridI9zuglCgwKKlpj3Ax1AT?se=2024-11-14T15%3A54%3A36Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D17bc54c8-cb38-49cd-adf1-2f42a2ab596a.webp&sig=uD09QepqIx/6BXPX9jp47voK5JXK4h2dshO0ijCmL90%3D")'''
    cursor.execute(insert_query)

    insert_query = '''INSERT INTO  pizzas_list (id, name, price, ingredients, image)
        VALUES (3, "Чотири соуси", "135", "Соус томатний, соус мексиканьский, соус американьский, чосниковий соус", "https://files.oaiusercontent.com/file-JDYl26QAJCRWU8bdw13GqnCR?se=2024-11-14T15%3A56%3A47Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D37cbb33e-944e-427f-98f4-8fbab810ba6f.webp&sig=sU4sSE%2ByCpOdrPp1hmlddS2tVdRNU8VbWKOykyTD8os%3D")'''
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

def get_all_pizzas():
    sqlite_connection = sqlite3.connect("sql_python.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM pizzas_list")
    pizzas = cursor.fetchall()
    return [{"id": row[0], "name": row[1], "price": row[2], "ingredients": row[3], "image": row[4]} for row in pizzas]

pizzas = get_all_pizzas()


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


