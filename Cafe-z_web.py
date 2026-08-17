from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from database import init_db, save_order, get_all_orders

app = Flask(__name__)
app.secret_key = "cafez-secret-key"

init_db()  # app start hote hi table bana degi (agar pehle se na ho)

menu = {
    "FAST FOOD": {
        "Pizza": 900,
        "Burger": 500,
        "Shawarma": 450,
        "Zinger Wrap": 600,
        "Smash Burger": 800,
        "Loaded Fries": 350,
        "Pasta": 500,
    },
    "DRINKS": {
        "Iced Matcha Latte": 450,
        "Boba Milk Tea": 500,
        "Cold Brew": 400,
        "Coke": 150,
        "Sprite": 130,
        "Pepsi": 130,
        "Fanta": 100,
        "Coffee": 200,
        "Green Tea": 150,
    },
}

def find_item_price(item_name):
    for category in menu:
        if item_name in menu[category]:
            return menu[category][item_name]
    return None

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

@app.route('/add/<item_name>')
def add_to_cart(item_name):
    if "cart" not in session:
        session["cart"] = []
    cart = session["cart"]
    cart.append(item_name)
    session["cart"] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart = session.get("cart", [])
    total = 0
    cart_items = []
    for item in cart:
        price = find_item_price(item)
        total += price
        cart_items.append({"name": item, "price": price})
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return redirect(url_for('view_cart'))

    customer_name = request.form.get("customer_name")
    total = sum(find_item_price(item) for item in cart)
    items_str = ", ".join(cart)
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_order(customer_name, items_str, total, order_date)

    session["cart"] = []  # cart khali kar do order confirm hone ke baad

    return redirect(url_for('order_success'))

@app.route('/success')
def order_success():
    return render_template('success.html')

@app.route('/orders')
def orders():
    all_orders = get_all_orders()
    return render_template('orders.html', orders=all_orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)