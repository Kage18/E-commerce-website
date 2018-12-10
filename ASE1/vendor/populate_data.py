from vendor.models import Category, Product
import csv


def populate_categories():
    categories = ['Home Needs', 'Groceries', 'Fruits/Veg', 'Beverages', 'Dairy', 'Personal care']
    for i in categories:
        c = Category(cat_name=i)
        c.save()


def gen_category_wise(category):
    c = Category.objects.get(cat_name=category)
    filename = 'vendor/static/vendor/Dairy.csv'
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            name = row[0]
            quantity = int(row[1])
            price = float(row[2])
            c.product_set.create(prod_name=name, stock=quantity, cost=price)
