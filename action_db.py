from models import Product, Company

'''Company'''
def company_exist(name: str) -> bool:
    return Company.select().where(Company.name == name).exists()

def add_company(name: str, password: str):
    Company.create(name=name, password=password)

def get_company_by_name(name: str):
    return Company.get_or_none(Company.name == name)


'''Item'''
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