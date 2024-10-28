from flask import Flask, render_template

app = Flask(__name__)

pizzas = [
    {"name": "Чотири Сира", "price": 170, "ingredients": "Соус вершковий, сир моцарела, сир дор блю, сир королівський, сир пармезан", "image_url": "https://tashirpizza.ru/images/products/44-1374.png"},
    {"name": "Салямі", "price": 135, "ingredients": "Основа, томатний соус, сир моцарелла, салямі", "image_url": "https://i0.wp.com/www.izumi-sushi.kz/wp-content/uploads/D181D0B0D0BBD18FD0BCD0B8.webp?fit=300%2C300&ssl=1"},
    {"name": "Пеппероні", "price": 220, "ingredients": "Соус томатний, сир моцарела, папероні", "image_url": "https://sergiopizza.ru/upload/iblock/4f4/4f4b7fa79e8465500baa585cf4f8b803.png"}
]

@app.get("/")
def first_page():
    return render_template("firstpage.html", title="Три ківбаски", order="Замовлення", news="Новини", menu_pizza="Меню піццерії")

@app.get("/menu/")
def menu_list():
    return render_template("menu.html", menu="Меню", our_pizza="Наша піцца", pizzas=pizzas)

if __name__ == '__main__':
    app.run(port=5051, debug=True)
