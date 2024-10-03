# Canvas Course Group Details Extractor

This Flask-based web application extracts student and group information from Canvas courses using the Canvas API. It provides a user-friendly interface for educators and administrators to easily access and analyze course data.

## Features

- Extracts student information including names, emails, and group assignments
- Retrieves group details such as group names and member counts
- Presents data in an organized tabular format
- Allows exporting of extracted data to CSV format

## Usage

1. Enter your Canvas API key
2. Provide the full URL of the Canvas course you want to analyze
3. Click "Extract Data" to retrieve and display the course information
4. Use the "Export Data" button to download the information in CSV format

## Technical Details

- Built with Flask
- Utilizes the Canvas API for data retrieval
- Implements error handling and logging for improved debugging
- Supports exporting data to CSV format for further analysis

## Setup

1. Clone the repository
2. Install the required dependencies
3. Set up the necessary environment variables
4. Run the Flask application

For detailed installation and configuration instructions, please refer to the project documentation.

## Student Data Privacy

The Canvas Course Group Details Extractor is designed with student data privacy in mind. However, it's crucial for users to understand their responsibilities when handling student information:

1. Data Collection: This tool only collects the necessary information from Canvas to provide the requested functionality. It does not gather any additional personal data beyond what is available through the Canvas API.

2. Data Storage: The application does not store any student data permanently. All information is processed in memory and is only temporarily stored during the CSV export process. Once the export is complete, the data is immediately deleted from the server.

3. Data Transmission: When using this tool, ensure you're on a secure network connection. The application uses HTTPS to encrypt data in transit, but it's your responsibility to protect your API key and any downloaded data.

4. User Responsibility: As a user of this tool, you are responsible for:
   - Obtaining necessary permissions from your institution before extracting student data
   - Ensuring compliance with your institution's data privacy policies and relevant regulations (e.g., FERPA in the US)
   - Safeguarding any exported data on your local machine
   - Not sharing student information with unauthorized parties

5. API Key Security: Your Canvas API key provides access to sensitive information. Never share your API key, and ensure it's kept secure at all times.

6. Data Retention: After using the tool, make sure to securely delete any exported files that contain student information when they are no longer needed.

7. Limited Use: Use this tool only for legitimate educational purposes as authorized by your institution.

By using the Canvas Course Group Details Extractor, you acknowledge your responsibility in protecting student data privacy and agree to handle all information in accordance with applicable laws and institutional policies.

