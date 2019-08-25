from flask import jsonify

from order_service import *

from bootstrap import app


@app.route('/orders', methods=['GET'])
def read():
    return jsonify(get_orders())


@app.route('/orders', methods=['POST', 'OPTIONS'])
def create():
    return create_order()


@app.route('/orders/<string:order_id>', methods=['PUT'])
def update(order_id):
    return update_order(order_id)


@app.route('/orders/<string:order_id>', methods=['DELETE'])
def delete(order_id):
    return delete_order(order_id)





if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)
