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
logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set debug mode
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'
app.config['DEBUG'] = DEBUG_MODE

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Render the main page of the Canvas Course Group Details Extractor."""
    logger.info("Rendering index page")
    return render_template('index.html', debug_mode=DEBUG_MODE)

@app.route('/extract', methods=['POST'])
def extract_data():
    """Extract and process course data from Canvas API."""
    logger.info("Received data extraction request")
    api_key = request.form.get('api_key')
    base_url = request.form.get('base_url')
    course_id = request.form.get('course_id')

    if not all([api_key, base_url, course_id]):
        logger.error("Missing required fields in extraction request")
        return jsonify({"error": "All fields (API Key, Base URL, and Course ID) are required"}), 400

    try:
        logger.info(f"Attempting to extract data for course {course_id}")
        course_data = get_course_data(api_key, base_url, course_id)
        logger.info("Data extraction successful")
        return render_template('results.html', data=course_data, debug_mode=DEBUG_MODE)
    except ValueError as e:
        logger.error(f"Value error during data extraction: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        logger.error(f"Runtime error during data extraction: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error during data extraction: {str(e)}")
        error_message = str(e) if DEBUG_MODE else "An unexpected error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

@app.route('/export', methods=['POST'])
def export_data():
    """Export the extracted course data to a CSV file."""
    logger.info("Received data export request")
    try:
        data = request.json
        if not data:
            logger.error("No data provided for export")
            return jsonify({"error": "No data provided for export"}), 400

        logger.info("Processing and exporting data")
        file_path = process_and_export_data(data)
        logger.info(f"Data exported successfully to {file_path}")
        
        @app.after_request
        def remove_file(response):
            try:
                os.remove(file_path)
                logger.info(f"Temporary file {file_path} removed")
            except Exception as e:
                logger.error(f"Error removing temporary file {file_path}: {str(e)}")
            return response
        
        return send_file(file_path, as_attachment=True, download_name="canvas_course_data.csv")
    except Exception as e:
        logger.error(f"Error during data export: {str(e)}")
        error_message = str(e) if DEBUG_MODE else "An error occurred while exporting data. Please try again later."
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
