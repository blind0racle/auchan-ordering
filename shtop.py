from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def shop_catalogue():
    items = [
        {'name': 'Product 1', 'image': 'cart.png', 'price': '19.99'},
        {'name': 'Морковка бляль', 'image': 'carrot.jpg', 'price': '5000.00'},
        {'name': 'Product 3', 'image': 'cac.jpg', 'price': '29.99'},
        {'name': 'Product 4', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 5', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 6', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 7', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 1', 'image': 'cart.png', 'price': '19.99'},
        {'name': 'Морковка бляль', 'image': 'carrot.jpg', 'price': '5000.00'},
        {'name': 'Product 3', 'image': 'cac.jpg', 'price': '29.99'},
        {'name': 'Product 4', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 5', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 6', 'image': 'product2.png', 'price': '29.99'},
        {'name': 'Product 7', 'image': 'product2.png', 'price': '29.99'},
        # Add more items as needed
    ]
    return render_template('shop.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
