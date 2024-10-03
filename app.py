import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from canvas_api import get_course_data
from data_processor import process_and_export_data
import logging

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_data():
    api_key = request.form['api_key']
    course_id = request.form['course_id']

    try:
        course_data = get_course_data(api_key, course_id)
        return render_template('results.html', data=course_data)
    except ValueError as e:
        logging.error(f"Value error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        logging.error(f"Runtime error: {str(e)}")
        return jsonify({"error": "An error occurred while fetching data from Canvas API. Please try again later."}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/export', methods=['POST'])
def export_data():
    try:
        data = request.json
        file_path = process_and_export_data(data)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Error during data export: {str(e)}")
        return jsonify({"error": "An error occurred while exporting data. Please try again later."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
