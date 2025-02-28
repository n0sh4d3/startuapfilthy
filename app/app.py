from flask import Flask, render_template, make_response


app = Flask(__name__)

NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
SIZE = "size"

shop_items = [
    {
    NAME: "Item1",
    DESCRIPTION: "Opis1",
    PRICE: 10.99,
    },
    {
    NAME: "Item2",
    DESCRIPTION: "Opis2",
    PRICE: 20.99,
    },
      {
    NAME: "Item2",
    DESCRIPTION: "Opis2",
    PRICE: 20.99,
    },
]
@app.route('/')
def home():
    response = make_response("welcom")
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', shop_items=shop_items)

@app.route('/item')
def shop():
    return render_template('item.html', shop_items=shop_items)


@app.route('/cart')
def cart():
    cart_items = shop_items
    total = 0
    for item_price in cart_items:
        total += item_price[PRICE]

    total = round(total, 2)
    return render_template('cart.html', cart_items=cart_items, total=total)


            #   <form action="" method="post">
            #   <button class="w-full bg-black text-white py-3 font-medium rounded-md hover:bg-gray-700 focus:outline-none">
            #     Dodaj do Koszyka
            #   </button>
            #   </form>

if __name__ == "__main__":
    app.run()