from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from action_db import *

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form.get('company_name').lower()
        password = request.form.get('password').lower()

        if company_exist(company_name):
            flash("Company already exists")
            return redirect(url_for('auth.register'))
        else:

            password_hash = generate_password_hash(password)

            flash("Company created")
            add_company(company_name, password_hash)
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        company_name = request.form.get('company_name').lower()
        password = request.form.get('password')

        if not company_exist(company_name):
            flash(f"Company {company_name} not exist")
            return redirect(url_for('auth.login'))

        company = get_company_by_name(company_name)
        if not check_password_hash(company.password, password):
            flash(f"Incorrect password")
            return redirect(url_for('auth.login'))


        session['company_name'] = company.name

        flash(f"Welcome, {company.name}")
        return redirect(url_for('product.index'))

    return render_template('auth/login.html')