from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = [{'email': 'worker1@example.com', 'password': 'password1', 'id': '1'},
           {'email': 'worker2@example.com', 'password': 'password2', 'id': '2'}]


@app.route('/')
def shop_catalogue():
    user_email = session.get('email', 'Guest')

    items = [
        {'name': 'Газ. напиток', 'image': 'product1.jpg', 'price': 100.00},
        {'name': 'Миндаль', 'image': 'product12.jpg', 'price': 159.00},
        {'name': 'Карт. чипсы', 'image': 'product3.png', 'price': 79.00},
        {'name': 'Карт. чипсы', 'image': 'product4.jpg', 'price': 79.00},
        {'name': 'Колбаса', 'image': 'product5.jpg', 'price': 259.00},

        {'name': 'Тостовый хлеб', 'image': 'product6.jpg', 'price': 129.00},
        {'name': 'Ржаной хлеб', 'image': 'product7.jpg', 'price': 75.00},
        {'name': 'Молоко', 'image': 'product8.jpg', 'price': 69.00},
        {'name': 'Хлопья', 'image': 'product9.jpg', 'price': 125.00},
        {'name': 'Тако', 'image': 'product10.jpg', 'price': 299.00},

        {'name': '', 'image': 'product11.jpg', 'price': 100.00},
        {'name': '', 'image': 'product2.jpg', 'price': 100000.00},
        {'name': '', 'image': 'product13.jpg', 'price': 100.00},
        {'name': '', 'image': 'product14.jpeg', 'price': 100.00},
        {'name': '', 'image': 'product15.jpg', 'price': 100.00},
    ]

    if 'cart' not in session:
        session['cart'] = {}

    total_price = 0
    for item_id, quantity in session['cart'].items():
        try:
            item_id_int = int(item_id)
            if item_id_int < len(items):
                total_price += items[item_id_int]['price'] * quantity
            else:
                print(f"Invalid item_id: {item_id}")
        except (ValueError, KeyError) as e:
            print(f"Error processing item_id {item_id}: {e}")

    return render_template('shop.html', items=items, cart=session['cart'], total_price=total_price, user_email=user_email)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if item_id:
        cart = session.get('cart', {})
        if item_id in cart:
            cart[item_id] += 1
        else:
            cart[item_id] = 1
        session['cart'] = cart
    return redirect(url_for('shop_catalogue'))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.form.get('item_id')
    if item_id:
        cart = session.get('cart', {})
        if item_id in cart:
            if cart[item_id] > 0:
                cart[item_id] -= 1
            if cart[item_id] == 0:
                del cart[item_id]
        session['cart'] = cart
    return redirect(url_for('shop_catalogue'))


@app.route('/view_cart')
def view_cart():
    items = [
        {'name': 'Газ. напиток', 'image': 'product1.jpg', 'price': 100.00},
        {'name': 'Миндаль', 'image': 'product12.jpg', 'price': 159.00},
        {'name': 'Карт. чипсы', 'image': 'product3.png', 'price': 79.00},
        {'name': 'Карт. чипсы', 'image': 'product4.jpg', 'price': 79.00},
        {'name': 'Колбаса', 'image': 'product5.jpg', 'price': 259.00},

        {'name': 'Тостовый хлеб', 'image': 'product6.jpg', 'price': 129.00},
        {'name': 'Ржаной хлеб', 'image': 'product7.jpg', 'price': 75.00},
        {'name': 'Молоко', 'image': 'product8.jpg', 'price': 69.00},
        {'name': 'Хлопья', 'image': 'product9.jpg', 'price': 125.00},
        {'name': 'Тако', 'image': 'product10.jpg', 'price': 299.00},

        {'name': '', 'image': 'product11.jpg', 'price': 100.00},
        {'name': '', 'image': 'product2.jpg', 'price': 100000.00},
        {'name': '', 'image': 'product13.jpg', 'price': 100.00},
        {'name': '', 'image': 'product14.jpeg', 'price': 100.00},
        {'name': '', 'image': 'product15.jpg', 'price': 100.00},
    ]

    if 'cart' not in session:
        session['cart'] = {}

    cart_items = []
    total_price = 0

    for item_id, quantity in session['cart'].items():
        try:
            item_id_int = int(item_id)
            if item_id_int < len(items):
                item = items[item_id_int]
                item['quantity'] = quantity
                item['total_price'] = quantity * item['price']
                cart_items.append(item)
                total_price += item['total_price']
            else:
                print(f"Invalid item_id: {item_id}")
        except (ValueError, KeyError) as e:
            print(f"Error processing item_id {item_id}: {e}")

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = next((user for user in users if user['email'] == email and user['password'] == password),
                          None)
            if user:
                session['user_id'] = user['id']
                session['email'] = email
                return redirect(url_for('shop_catalogue'))
            else:
                return 'Invalid email or password'

    return render_template('login.html')

@app.route('/order', methods=['POST'])
def order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    location = request.form.get('location')

    if 'cart' in session and session['cart']:

        session.pop('cart', None)
        return render_template('order-placed.html')
    else:
        return render_template('cart-empty.html')


if __name__ == '__main__':
    app.run(debug=True)