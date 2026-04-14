from flask import Flask, render_template, request, flash, redirect, url_for
from models import init_db
from action_db import *
app = Flask(__name__)
app.secret_key = '123'
init_db()
products = []

@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name').lower()
        price = float(request.form.get('price'))
        category = request.form.get('category').lower()

        if product_exist(name):
            flash("Item already exists", category="error")
        else:
            flash("Item added", category="success")
            add_product(name, price, category)
            products.append({"name": name, "price": price, "category": category})

        return redirect(url_for('index'))

    all_categories = get_all_categories()
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_products = get_all_products()
    else:
        filter_products = get_product_by_category(choice_category)

    return render_template('index.html',
                           products=filter_products,
                           categories=all_categories,
                           choice_category=choice_category)

@app.route('/delete/<int:index>')
def delete(index):
    flash(f"Item deleted", category="success")
    return redirect(url_for('index'))

app.run(debug=True)