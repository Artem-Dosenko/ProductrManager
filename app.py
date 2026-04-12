from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = '123'
products = []

@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')

        for item in products:
            if item.get('name') == name:
                flash("Item already exists")
                break
        else:
            info_product = {"name": name, "price": price, "category": category}
            products.append(info_product)

        return redirect(url_for('index'))

    return render_template('index.html')

app.run(debug=True)