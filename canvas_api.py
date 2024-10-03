import requests
import logging
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_course_data(api_key, base_url, course_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Validate base_url and course_id
        if not base_url or not course_id:
            raise ValueError("Base URL and Course ID are required.")

        # Get students
        logging.info(f"Fetching students for course {course_id}")
        students_url = urljoin(base_url, f"/api/v1/courses/{course_id}/users?enrollment_type[]=student")
        logging.debug(f"GET request to: {students_url}")
        students_response = requests.get(students_url, headers=headers)
        students_response.raise_for_status()
        students = students_response.json()
        logging.info(f"Successfully fetched {len(students)} students")
        
        # Get groups
        logging.info(f"Fetching groups for course {course_id}")
        groups_url = urljoin(base_url, f"/api/v1/courses/{course_id}/groups")
        logging.debug(f"GET request to: {groups_url}")
        groups_response = requests.get(groups_url, headers=headers)
        groups_response.raise_for_status()
        groups = groups_response.json()
        logging.info(f"Successfully fetched {len(groups)} groups")
        
        # Get group memberships
        logging.info(f"Fetching group categories for course {course_id}")
        memberships_url = urljoin(base_url, f"/api/v1/courses/{course_id}/group_categories")
        logging.debug(f"GET request to: {memberships_url}")
        memberships_response = requests.get(memberships_url, headers=headers)
        memberships_response.raise_for_status()
        group_categories = memberships_response.json()
        logging.info(f"Successfully fetched {len(group_categories)} group categories")
        
        # Process data
        student_group_info = []
        for student in students:
            student_info = {
                "id": student["id"],
                "name": student["name"],
                "email": student.get("email", "N/A"),
                "groups": []
            }
            
            for group in groups:
                if any(member["user_id"] == student["id"] for member in group.get("members", [])):
                    student_info["groups"].append(group["name"])
            
            student_group_info.append(student_info)
        
        logging.info("Data processing completed successfully")
        return {
            "students": student_group_info,
            "groups": groups,
            "group_categories": group_categories
        }
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching data from Canvas API: {str(e)}")
        if isinstance(e, requests.exceptions.HTTPError):
            status_code = e.response.status_code
            error_message = e.response.text
            logging.error(f"HTTP Error {status_code}: {error_message}")
            if status_code == 401:
                raise ValueError("Invalid API key or unauthorized access")
            elif status_code == 404:
                raise ValueError(f"Course with ID {course_id} not found")
        elif isinstance(e, requests.exceptions.ConnectionError):
            logging.error("Connection error occurred. Please check your internet connection.")
            raise RuntimeError("Failed to connect to Canvas API. Please check your internet connection.")
        elif isinstance(e, requests.exceptions.Timeout):
            logging.error("Request timed out. Canvas API might be slow or unresponsive.")
            raise RuntimeError("Request to Canvas API timed out. Please try again later.")
        raise RuntimeError(f"Failed to fetch data from Canvas API: {str(e)}")
    
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise
