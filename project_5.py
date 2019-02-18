import json
import sqlite3
import sys
import jinja2

product_id = sys.argv[1]

conn = sqlite3.connect('session_5.db')
c = conn.cursor()

c.execute("DELETE FROM product")

product_dict = json.load(open('product.json'))
for prodid in product_dict:
    this_product_dict = product_dict[prodid]
    brand = product_dict[prodid]["brand"]
    list_price = product_dict[prodid]["list_price"]
    product_descript = product_dict[prodid]["product_description"]
    prod_id = product_dict[prodid]["product_id"]
    prod_name = product_dict[prodid]["product_name"]
    sale_price = product_dict[prodid]["sale_price"]

    query = "INSERT INTO product (brand, product_name, product_descript, product_id, list_price, sale_price) VALUES (?, ?, ?, ?, ?, ?)"

    c.execute(query, (brand, prod_name, product_descript, prod_id, list_price, sale_price))
    conn.commit()


def query_database(product_id):
    row = c.execute('SELECT * FROM product WHERE product_id =?', (product_id,))
    result = row.fetchone()
    return result


def split_it_up(result):
    brand, list_price, description, id, name, sale_price = result
    return id, brand, list_price, description, name, sale_price


class Product (object):
    def __init__(self, id):
        result = query_database(product_id)
        id, brand, list_price, description, name, sale_price = split_it_up(result)
        self.id = id
        self.brand = brand
        self.list_price = list_price
        self.description = description
        self.name = name
        self.sale_price = sale_price

    def __str__(self):
        formatted_string = "{}{}{}{}{}{}".format(self.id, self.name, self.brand, self.description, self.sale_price, self.list_price, self.get_savings_pct())
        return formatted_string

    def get_savings_pct(self):
        spct = ((((self.list_price - self.sale_price) / self.list_price) * 100))
        spct = float(round(spct, 2))
        return spct



this_product = Product(product_id)
template_dir = 'templates'
env = jinja2.Environment()
env.loader = jinja2.FileSystemLoader(template_dir)

template = env.get_template('product.html')
completed_page = template.render(product=this_product)
wfh = open(prod_id + '.html', 'w')
wfh.write(completed_page)
wfh.close()


# Product IDs
# 21660
# 23346
# 67044
# JAN172663
# MAY172533
