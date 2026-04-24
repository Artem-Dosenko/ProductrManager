from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from action_db import *

product_bp = Blueprint('product', __name__, template_folder='templates')

def is_logged():
    return 'company_name' in session

def current_company():
    name_company = session.get('company_name')
    if not name_company:
        return None
    return get_company_by_name(name_company)

@product_bp.route('/', methods=['GET', 'POST'])
@product_bp.route('/products', methods=['GET', 'POST'])
def index():

    if not is_logged():
        return redirect(url_for('auth.login'))

    company = current_company()

    if request.method == 'POST':
        name = request.form.get('name').lower()
        price = float(request.form.get('price'))
        category = request.form.get('category').lower()

        if product_exist(name, company.id):
            flash("Item already exists")
        else:
            add_product(name, price, category, company.id)

        return redirect(url_for('product.index'))

    all_categories = get_all_categories(company.id)
    choice_category = request.args.get('category', 'all')

    if choice_category == 'all':
        filter_products = get_all_products(company.id)
    else:
        filter_products = get_product_by_category(choice_category, company.id)

    return render_template('product/index.html',
                           products=filter_products,
                           categories=all_categories,
                           choice_category=choice_category)

@product_bp.route('/delete/<name>')
def delete(name):
    if not is_logged():
        return redirect(url_for('auth.login'))

    company = current_company()
    delete_product(name, company.id)

    flash(f'Item {name} deleted')
    return redirect(url_for('product.index'))

@product_bp.route('/edit')
def edit():
    return render_template('product/edit.html')