from flask import request
from order_repository import *
from bootstrap import mysql


def get_orders():
	return list_orders()


def create_order():
	data = request.form.get('product_id').split(',')
	total_price = calculate_total(data)
	insert_order(len(data), total_price, data)

	return 'Order created'


def calculate_total(data):
	prices = []
	for item in data:
		cur = mysql.connection.cursor()
		sql_query = 'SELECT product_price FROM products WHERE product_id=%s'
		cur.execute(sql_query, item)
		fetchdata = cur.fetchone()
		prices.append(int(fetchdata[0]))
		cur.close()

	return sum(prices)


def update_order(order_id):
	new_products = request.form.get('product_id').split(',')
	new_total_price = calculate_total(new_products)
	update_db(len(new_products), new_total_price, new_products, order_id)
	return 'Order ' + order_id + ' updated.'


def delete_order(order_id):
	delete_from_db(order_id)
	return 'Order ' + order_id + ' deleted.'

