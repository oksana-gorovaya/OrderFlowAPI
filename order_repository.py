from flask import jsonify

from bootstrap import mysql


def list_orders():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM orders')
	fetchdata = cur.fetchall()
	cur.close()
	return fetchdata


def insert_order(number_of_products, total_price, data):
	cur = mysql.connection.cursor()
	sql_query = 'INSERT INTO orders (number_of_products, total_price) VALUES (%s, %s)'
	cur.execute(sql_query, (number_of_products, total_price))
	mysql.connection.commit()
	create_order_details(cur, data)
	cur.close()
	if cur.rowcount < 1:
		raise Exception('Sorry, failed to create order.')


def create_order_details(cur, data):
	sql_query = 'INSERT INTO order_products (order_id, product_id) VALUES (%s, %s)'
	cur.execute('SELECT MAX(order_id) FROM orders')
	order_id = cur.fetchone()
	for product_id in data:
		cur.execute(sql_query, (order_id, product_id))
		mysql.connection.commit()
	if cur.rowcount < 1:
		raise Exception('Sorry, failed to create order.')


def update_db(new_number_of_products, new_total_price, new_products, order_id):
	cur = mysql.connection.cursor()
	sql_query = "UPDATE orders SET number_of_products = %s, total_price = %s WHERE order_id = %s"
	cur.execute(sql_query, (new_number_of_products, new_total_price, order_id))
	update_order_details(cur, new_products, order_id)
	if cur.rowcount < 1:
		raise Exception('Sorry, failed to update order.')
	cur.close()


def update_order_details(cur, new_products, order_id):
	sql_query = "UPDATE order_products SET product_id = %s WHERE order_id = %s"
	for product_id in new_products:
		cur.execute(sql_query, (product_id, order_id))
		mysql.connection.commit()


def delete_from_db(order_id):
	cur = mysql.connection.cursor()
	sql_query = "DELETE orders, order_products FROM orders INNER JOIN order_products ON orders.order_id = order_products.order_id WHERE orders.order_id= %s"
	cur.execute(sql_query, (order_id,))
	mysql.connection.commit()
	if cur.rowcount < 1:
		raise Exception('Sorry, failed to delete order.')
	cur.close()
