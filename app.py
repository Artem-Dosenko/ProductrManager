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
        price = request.form.get('price')
        category = request.form.get('category').lower()

        for item in products:
            if item.get('name') == name:
                flash("Item already exists")
                break
        else:
            info_product = {"name": name, "price": price, "category": category}
            products.append(info_product)

        return redirect(url_for('index'))

    all_categories = map(lambda item: item['category'], products)
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_products = products
    else:
        filter_products = filter(lambda item: item['category'] == choice_category, products)

    return render_template('index.html',
                           products=filter_products,
                           categories=all_categories,
                           choice_category=choice_category)

@app.route('/delete/<int:index>')
def delete(index):
    deleted_item = products.pop(index)
    flash(f"Item {deleted_item["name"]} deleted")
    return redirect(url_for('index'))

app.run(debug=True)