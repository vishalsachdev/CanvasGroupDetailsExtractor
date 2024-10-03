import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from canvas_api import get_course_data
from data_processor import process_and_export_data

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
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/export', methods=['POST'])
def export_data():
    data = request.json
    file_path = process_and_export_data(data)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
