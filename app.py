from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db
from action_db import *
app = Flask(__name__)
app.secret_key = '123'
init_db()
products = []

def is_logged():
    return 'company_name' in session

@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def index():

    if not is_logged():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name').lower()
        price = float(request.form.get('price'))
        category = request.form.get('category').lower()

        if product_exist(name):
            flash("Item already exists")
        else:
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
    deleted_item = products.pop(index)
    flash(f"Item {deleted_item["name"]} deleted")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form.get('company_name').lower()
        password = request.form.get('password').lower()

        if company_exist(company_name):
            flash("Company already exists")
            return redirect(url_for('register'))
        else:

            password_hash = generate_password_hash(password)

            flash("Company created")
            add_company(company_name, password_hash)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        company_name = request.form.get('company_name').lower()
        password = request.form.get('password')

        if not company_exist(company_name):
            flash(f"Company {company_name} not exist")
            return redirect(url_for('login'))

        company = get_company_by_name(company_name)
        if not check_password_hash(company.password, password):
            flash(f"Incorrect password")
            return redirect(url_for('login'))


        session['company_name'] = company.name

        flash(f"Welcome, {company.name}")
        return redirect(url_for('index'))

    return render_template('login.html')

app.run(debug=True)