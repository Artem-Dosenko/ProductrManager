from models import Product

def get_all_products():
    return Product.select()

def get_product_by_category(category):
    return Product.select().where(Product.category == category)

def get_all_categories():
    return Product.select().distinct().order_by(Product.category)

def product_exist(name) -> bool:
    return Product.select().where(Product.name == name).exists()

def add_product(name: str, price: float, category: str):
    Product.create(name=name, price=price, category=category)

def delete_product(product_id: int):
    Product.delete().where(Product.id == product_id).execute()