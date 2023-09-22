from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'very_secret_key'

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        count = int(request.form['count'])

        product = Product(title=title, description=description, price=price, count=count)
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        products = Product.query.filter(Product.title.ilike(f'%{search_term}%')).all()
    else:
        products = []

    return render_template('search.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
