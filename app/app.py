from flask import Flask, render_template, make_response, abort

app = Flask(__name__)

NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
SIZE = "size"

shop_items = [
    {
        NAME: "spust pycha",
        DESCRIPTION: "nie wiem co sie dzieje ale kurwa buja nie",
        PRICE: 21.37,
    },
    {
        NAME: "brudna woda",
        DESCRIPTION: "nazwa muwi sama za sb",
        PRICE: 20.99,
    },
    {
        NAME: "order cwela",
        DESCRIPTION: "ciezko zapracowalem na ten tytul",
        PRICE: 90.99,
    },
    {
        NAME: "zestaw goonera",
        DESCRIPTION: "zeby hojnie zyc trzeba hojnie wydac",
        PRICE: 0.00, # robiac to licze sie z faktem ze kosz sie rozjebie ale to smiesznie
    },
    {
        NAME: "cyberszlug",
        DESCRIPTION: "smakowe poietrze goes brrrrr",
        PRICE: 1.99,
    },
    {
        NAME: "chinska republika ludowa",
        DESCRIPTION: "Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING 🥶🍦 wǒ hěn xǐhuān BING CHILLING 🥶🍦",
        PRICE: 4.50,
    },
    {
        NAME: "samohud",
        DESCRIPTION: "ten ruw wyglada bardzo hottt",
        PRICE: 1999.99,
    },
]

@app.route('/')
def home():
    response = make_response("Welcome")
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
    shop_items = shop_items
    return render_template('shop.html', shop_items=shop_items)

@app.route('/item/<item_name>')
def item(item_name):
    
    # modl sie ze nastepny item istnieje
    item = next((item for item in shop_items if item[NAME].lower() == item_name.lower()), None)

    if item is None:
        print(f"Item not found: {item_name}")  # pytanie kurwa jak skoro jest. patrze sie na to kurwa
        return render_template('error.html')

    print(f"Item details: {item}")

    return render_template('item.html', item=item)

@app.route('/cart')
def cart():
    cart_items = shop_items
    total = 0
    for item in cart_items:
        total += item[PRICE]

    total = round(total, 2)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True, port=42069)
