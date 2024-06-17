from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace this with your secret key

users = [{'email': 'worker1@example.com', 'password': 'password1', 'id': '1'},
           {'email': 'worker2@example.com', 'password': 'password2', 'id': '2'}]


@app.route('/')
def shop_catalogue():
    items = [
        {'name': 'Морковка бляль', 'image': 'carrot.jpg', 'price': 5000.00},
        {'name': 'Картошка', 'image': 'potato.jpg', 'price': 2000.00},
        {'name': 'Лук', 'image': 'onion.jpg', 'price': 1000.00},
        # Add more unique items as needed
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

    return render_template('shop.html', items=items, cart=session['cart'], total_price=total_price)


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
                del cart[item_id]  # Remove item from cart if quantity is zero
        session['cart'] = cart
    return redirect(url_for('shop_catalogue'))


@app.route('/view_cart')
def view_cart():
    items = [
        {'name': 'Морковка бляль', 'image': 'carrot.jpg', 'price': 5000.00},
        {'name': 'Картошка', 'image': 'potato.jpg', 'price': 2000.00},
        {'name': 'Лук', 'image': 'onion.jpg', 'price': 1000.00},
        # Add more unique items as needed
    ]

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
            worker = next((worker for worker in users if worker['email'] == email and worker['password'] == password),
                          None)
            if worker:
                return f'Logged in as {email} (Worker ID: {worker["id"]})'
            else:
                return 'Invalid email or password'

    return render_template('login.html')

@app.route('/order', methods=['POST'])
def order():
    location = request.form.get('location')
    if 'cart' in session and session['cart']:
        # Process the order here.
        session.pop('cart', None)  # Clear the cart after order
        return 'Order Placed Successfully'
    else:
        return 'Cart is empty', 400  # Handle empty cart scenario


if __name__ == '__main__':
    app.run(debug=True)