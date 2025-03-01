# napraw kurwa te obrazki w item.html bo wygladaja jak cwel
# napraw te strzalke przy view all
from flask import Flask, render_template, make_response, abort

app = Flask(__name__)

NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
SIZE = "size"
IMAGE = "image"
DISCOUNT = "discount"

# notatki dla keyn.wazne@gmail.com
# jesli item jest nowy to daj "new": True
# jezeli nie dasz to item sie nie oznaczy jako nowy i burdel w kodzie powstanei

# jak chcesz dac promke dajesz DISCOUNT: (cena i zamiast , uzywa sie kropek)
# inaczej dostaniesz syntax error

# mega wazne zeby kazda linijka konczyla sie przecinkiem bo dostaniesz syntax error
# kolejnosc rzeczy nie ma znaczenia, ale wszystko staraj sie robic tak samo zeby bylo consistent

# to main item na stronie
featured_item = {
   NAME: "hesy" ,
   DESCRIPTION: "pracowac musi",
   PRICE: 9090,
   IMAGE: "hesy.jpg",
   "new": True,
}


# itemki do pokazania
# pierwsze 4 itemki tutaj sa pokazywanie  w sekcji "kurwa drip"
shop_items = [
    {
        NAME: "spust pycha",
        DESCRIPTION: "nie wiem co sie dzieje ale kurwa buja nie",
        PRICE: 21.37,
        IMAGE: "beediddy.jpg",
        "new": True,
    },
    {
        NAME: "brudna woda",
        DESCRIPTION: "nazwa muwi sama za sb",
        PRICE: 20.99,
        IMAGE: "hitler.jpg",
        "new": False,
    },
    {
        NAME: "order cwela",
        DESCRIPTION: "ciezko zapracowalem na ten tytul",
        PRICE: 90.99,
        IMAGE: "wtcwel.jpg",
        "new": True,
        DISCOUNT: 30.99, # to jest opcjonalne i mozesz sie domyslic co to zrobi jak to dasz
    },
    {
        NAME: "zestaw goonera",
        DESCRIPTION: "zeby hojnie zyc trzeba hojnie wydac",
        PRICE: 0.00, # robiac to licze sie z faktem ze kosz sie rozjebie ale to smiesznie
        IMAGE: "sigmy.jpg",
        "new": False,
    },
    {
        NAME: "cyberszlug",
        DESCRIPTION: "smakowe poietrze goes brrrrr",
        PRICE: 1.99,
        IMAGE: "gej.jpg",
        "new": False,
        DISCOUNT: 10.99,
    },
    {
        NAME: "chinska republika ludowa",
        DESCRIPTION: "Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING 🥶🍦 wǒ hěn xǐhuān BING CHILLING 🥶🍦",
        PRICE: 2.50,
        IMAGE: "duma.jpg",
        "new": True,
    },
    {
        NAME: "samohud",
        DESCRIPTION: "ten ruw wyglada bardzo hottt",
        PRICE: 1999.99,
        IMAGE: "certyfikat.jpg",
        "new": False,
    },
]

# tutaj sie kurwa przygoda zaczyna
@app.route('/')
def home():
    # chce kurwa tylko 4 czaoisz
    featured_items = shop_items[:4]
    response = make_response("Welcome")
    return render_template('index.html', featured_item=featured_item, featured_items= featured_items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', status_code=404)

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', status_code=500)

if __name__ == "__main__":
    app.run(debug=True, port=42069)
