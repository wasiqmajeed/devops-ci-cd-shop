from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model (The "Product" table)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@app.route('/add_sample')
def add_sample():
    # Helper route to populate the shop for testing
    p1 = Product(name="Vintage Camera", price=120.00, description="A classic 35mm film camera.")
    p2 = Product(name="Leather Satchel", price=85.00, description="Handcrafted brown leather bag.")
    db.session.add_all([p1, p2])
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the .db file automatically
    app.run(debug=True)