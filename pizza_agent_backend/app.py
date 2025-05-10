from flask import Flask, Blueprint, jsonify, request
from bigQuery import BigQueryInterface
from routes.menu_routes import menu_bp
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register the blueprint
app.register_blueprint(menu_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Server is running. Try /api/test or /api/menu_display"})

app.run(host='0.0.0.0', port=5005, debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)