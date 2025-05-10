from flask import Blueprint, jsonify, request
from bigQuery import BigQueryInterface

# Create Blueprint for menu routes
menu_bp = Blueprint('menu', __name__)

# Initialize BigQuery interface
# bigquery_interface = BigQueryInterface('gcp-df-w2', 'Pizza_menu', 'pizza_menu')

@menu_bp.route('/menu_display', methods=['POST'])
def display_menu():
    """
    Endpoint to display the pizza menu
    """
    print('Received request to /api/menu_display')
    try:
        body = request.get_json()
        return {'hello': 'world'}
        # menu_data = bigquery_interface.get_pizza_menu()
        # payload = {
        #     {"fulfillmentMessages": [
        #         {
        #             "payload": {
        #                 "menu": menu_data
        #             }
        #         }
        #     ]}
        # }
        # return jsonify(payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/order', methods=['POST'])
def order_pizza():
    """
    Endpoint to add a new pizza to the menu
    """
    print('bye')
    try:
        return {'pizza':'ordered'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/editOrder', methods=['POST'])
def edit_order():
    """
    Endpoint to update an existing pizza
    """

    try:
        # pizza_data = request.get_json()
        # bigquery_interface.update_pizza(pizza_id, pizza_data)
        # return jsonify({"message": "Pizza updated successfully"})
        return {'order': 'edited'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/delete_pizza/<int:pizza_id>', methods=['DELETE'])
def delete_pizza(pizza_id):
    """
    Endpoint to delete a pizza from the menu
    """
    try:
        bigquery_interface.delete_pizza(pizza_id)
        return jsonify({"message": "Pizza deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500 