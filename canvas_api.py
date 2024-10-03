import requests
import logging
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_course_data(api_key, base_url, course_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Validate base_url and course_id
        if not base_url or not course_id:
            raise ValueError("Base URL and Course ID are required.")

        # Get students
        logger.info(f"Fetching students for course {course_id}")
        students_url = urljoin(base_url, f"/api/v1/courses/{course_id}/users?enrollment_type[]=student")
        logger.debug(f"GET request to: {students_url}")
        students_response = requests.get(students_url, headers=headers, timeout=10)
        students_response.raise_for_status()
        students = students_response.json()
        logger.info(f"Successfully fetched {len(students)} students")
        
        # Get groups
        logger.info(f"Fetching groups for course {course_id}")
        groups_url = urljoin(base_url, f"/api/v1/courses/{course_id}/groups")
        logger.debug(f"GET request to: {groups_url}")
        groups_response = requests.get(groups_url, headers=headers, timeout=10)
        groups_response.raise_for_status()
        groups = groups_response.json()
        logger.info(f"Successfully fetched {len(groups)} groups")
        
        # Get group memberships for each group
        group_memberships = {}
        for group in groups:
            group_id = group['id']
            logger.info(f"Fetching memberships for group {group_id}")
            memberships_url = urljoin(base_url, f"/api/v1/groups/{group_id}/memberships")
            logger.debug(f"GET request to: {memberships_url}")
            memberships_response = requests.get(memberships_url, headers=headers, timeout=10)
            memberships_response.raise_for_status()
            group_memberships[group_id] = memberships_response.json()
            logger.info(f"Successfully fetched {len(group_memberships[group_id])} memberships for group {group_id}")
        
        # Process data
        student_group_info = []
        group_info = []
        for group in groups:
            group_id = group['id']
            group_name = group['name']
            member_count = len(group_memberships[group_id])
            group_info.append({
                "id": group_id,
                "name": group_name,
                "members_count": member_count
            })
            logger.debug(f"Group {group_name} has {member_count} members")

        for student in students:
            student_info = {
                "id": student["id"],
                "name": student["name"],
                "email": student.get("email", "N/A"),
                "groups": []
            }
            
            for group in groups:
                group_id = group['id']
                if any(member["user_id"] == student["id"] for member in group_memberships[group_id]):
                    student_info["groups"].append(group["name"])
                    logger.debug(f"Student {student['id']} assigned to group {group['name']}")
            
            student_group_info.append(student_info)
            logger.debug(f"Processed student {student['id']} with groups: {student_info['groups']}")
        
        logger.info("Data processing completed successfully")
        return {
            "students": student_group_info,
            "groups": group_info
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching data from Canvas API: {str(e)}")
        if isinstance(e, requests.exceptions.HTTPError):
            status_code = e.response.status_code
            error_message = e.response.text
            logger.error(f"HTTP Error {status_code}: {error_message}")
            if status_code == 401:
                raise ValueError("Invalid API key or unauthorized access")
            elif status_code == 404:
                raise ValueError(f"Course with ID {course_id} not found")
            elif status_code == 403:
                raise ValueError("Insufficient permissions to access the requested resource")
            elif status_code >= 500:
                raise RuntimeError("Canvas API is currently experiencing issues. Please try again later.")
        elif isinstance(e, requests.exceptions.ConnectionError):
            logger.error("Connection error occurred. Please check your internet connection.")
            raise RuntimeError("Failed to connect to Canvas API. Please check your internet connection.")
        elif isinstance(e, requests.exceptions.Timeout):
            logger.error("Request timed out. Canvas API might be slow or unresponsive.")
            raise RuntimeError("Request to Canvas API timed out. Please try again later.")
        raise RuntimeError(f"Failed to fetch data from Canvas API: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

