# napraw kurwa te obrazki w item.html bo wygladaja jak cwel
# napraw te strzalke przy view all

# jebnij pip install -r requirements.txt
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'cwel_sekret_key_kurwa'  # niezbedne mi to
csrf = CSRFProtect(app)
NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
SIZE = "size"
IMAGE = "image"
DISCOUNT = "discount"
COLOR = "color"

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

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Proszę się zalogować, aby uzyskać dostęp do tej strony.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_cart_items():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def get_cart_count():
    try:
        if 'user_id' in session:
            conn = get_db_connection()
            
            try:
                result = conn.execute('''
                    SELECT SUM(quantity) as total_count 
                    FROM cart 
                    WHERE user_id = ?
                ''', (session['user_id'],)).fetchone()
                conn.close()
                
                return result['total_count'] or 0
                
            except sqlite3.OperationalError as e:
                if "no such table: cart" in str(e):
                    conn.execute('''
                    CREATE TABLE IF NOT EXISTS cart (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                    ''')
                    conn.commit()
                conn.close()
                return 0
        
        elif 'cart' in session:
            return sum(item.get('quantity', 0) for item in session.get('cart', []))
        
        return 0
        
    except Exception as e:
        print(f"Error getting cart count: {e}")
        return 0

def get_cart_total():
    cart = get_cart_items()
    total = 0
    for item_key, item_data in cart.items():
        item_name = item_data['name']
        quantity = item_data['quantity']
        
        item = next((item for item in shop_items if item[NAME].lower() == item_name.lower()), None)
        if item:
            price = item.get(DISCOUNT, item[PRICE])
            total += price * quantity
    return round(total, 2)

def get_cart_products():
    cart = get_cart_items()
    cart_products = []
    
    for item_key, item_data in cart.items():
        item_name = item_data['name']
        item = next((item for item in shop_items if item[NAME].lower() == item_name.lower()), None)
        
        if item:
            cart_item = item.copy()
            cart_item['quantity'] = item_data['quantity']
            cart_item['size'] = item_data.get('size', 'One Size')
            cart_item['color'] = item_data.get('color', 'Default')
            cart_item['item_total'] = round(item_data['quantity'] * cart_item.get(DISCOUNT, cart_item[PRICE]), 2)
            cart_products.append(cart_item)
    
    return cart_products

# tutaj sie kurwa przygoda zaczyna
@app.route('/')
def home():
    # chce kurwa tylko 4 czaoisz
    featured_items = shop_items[:2]
    cart_count = get_cart_count()
    return render_template('index.html', featured_item=featured_item, featured_items=featured_items, cart_count=cart_count)

@app.route('/about')
def about():
    cart_count = get_cart_count()
    return render_template('about.html', cart_count=cart_count)

@app.route('/contact')
def contact():
    cart_count = get_cart_count()
    return render_template('contact.html', cart_count=cart_count)

@app.route('/shop')
def shop():
    cart_count = get_cart_count()
    return render_template('shop.html', shop_items=shop_items, cart_count=cart_count)

@app.route('/item/<item_name>')
def item(item_name):
    # modl sie ze nastepny item istnieje
    item = next((item for item in shop_items if item[NAME].lower() == item_name.lower()), None)
    if item is None:
        print(f"Item not found: {item_name}")
        return render_template('error.html')
    
    cart_count = get_cart_count()
    print(f"Item details: {item}")
    return render_template('item.html', item=item, cart_count=cart_count)

@app.route('/add_to_cart/<item_name>', methods=['POST'])
def add_to_cart(item_name):
    item = next((item for item in shop_items if item[NAME].lower() == item_name.lower()), None)
    if not item:
        return redirect(url_for('shop'))
    
    # zajeb kruwa z sesji
    cart = get_cart_items()
    
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size', 'One Size')
    color = request.form.get('color', 'Default')
    
    # tutaj sie dzieja czary 
    # w skruncie jest kurwa  tworzony "klucz" skladajacy sie z nazwy itemu + rozmiaru + koloru
    # i w ten sposob backend poznaje co jest w koshu
    cart_key = f"{item_name.lower()}_{size}_{color}"
    
    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'name': item_name.lower(),
            'quantity': quantity,
            'size': size,
            'color': color
        }
    
    session['cart'] = cart
    
    # wracaj kurwa na item ktury sb przeglondash
    return redirect(url_for('cart', jiggle=1))

@app.route('/update_cart_item', methods=['POST'])
def update_cart_item():
    cart = get_cart_items()
    cart_key = request.form.get('cart_key')
    action = request.form.get('action')
    
    if cart_key in cart:
        if action == 'increase':
            cart[cart_key]['quantity'] += 1
        elif action == 'decrease':
            if cart[cart_key]['quantity'] > 1:
                cart[cart_key]['quantity'] -= 1
            else:
                del cart[cart_key]
        elif action == 'remove':
            del cart[cart_key]
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_products = get_cart_products()
    cart_total = get_cart_total()
    cart_count = get_cart_count()
    
    return render_template('cart.html', cart_items=cart_products, total=cart_total, cart_count=cart_count, cart=get_cart_items())

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('cart'))

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    
    if not query:
        return redirect(url_for('shop'))
    results = [item for item in shop_items if query in item[NAME].lower()]
    if len(results) == 1:
        return redirect(url_for('item', item_name=results[0][NAME].lower()))
    
    cart_count = get_cart_count()
    return render_template('search_results.html', results=results, query=query, cart_count=cart_count)

@app.context_processor
def inject_shop_items():
    return dict(shop_items=shop_items)

@app.route('/login')
def login():
    cart_count = get_cart_count()
    return render_template('login.html', cart_count=cart_count)

@app.route('/register')
def register():
    cart_count = get_cart_count()
    return render_template('register.html', cart_count=cart_count)

@app.route('/login', methods=['POST'])
def login_post():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember-me') else False
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user['password'], password):
            flash('Nieprawidłowy email lub hasło. Spróbuj ponownie.', 'error')
            return redirect(url_for('login'))
        
        # Create session for the user
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        
        if remember:
            session.permanent = True
        
        flash('Zalogowano pomyślnie!', 'success')
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
            
        return redirect(url_for('item'))  # Or any other route that exists in your app
        
    except Exception as e:
        flash(f'Wystąpił błąd podczas logowania: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register_post():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        if password != confirm_password:
            flash('Hasła nie pasują do siebie.', 'error')
            return redirect(url_for('register'))
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user:
            conn.close()
            flash('Email już istnieje w bazie.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                    (name, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Konto zostało utworzone pomyślnie! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(f'Wystąpił błąd podczas rejestracji: {str(e)}', 'error')
        return redirect(url_for('register'))

@app.errorhandler(404)
def page_not_found(error):
    cart_count = get_cart_count()
    return render_template('error.html', status_code=404, cart_count=cart_count)

@app.errorhandler(500)
def internal_error(error):
    cart_count = get_cart_count()
    return render_template('error.html', status_code=500, cart_count=cart_count)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=42069)

# notatki dla keyn.wazne@gmail.com
# jesli item jest nowy to daj "new": True
# jezeli nie dasz to item sie nie oznaczy jako nowy i burdel w kodzie powstanei

# jak chcesz dac promke dajesz DISCOUNT: (cena i zamiast , uzywa sie kropek)
# inaczej dostaniesz syntax error

# mega wazne zeby kazda linijka konczyla sie przecinkiem bo dostaniesz syntax error
# kolejnosc rzeczy nie ma znaczenia, ale wszystko staraj sie robic tak samo zeby bylo consistent

# to main item na stronie