import requests

BASE_URL = "https://canvas.instructure.com/api/v1"

def get_course_data(api_key, course_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Get students
    students_url = f"{BASE_URL}/courses/{course_id}/users?enrollment_type[]=student"
    students_response = requests.get(students_url, headers=headers)
    students_response.raise_for_status()
    students = students_response.json()
    
    # Get groups
    groups_url = f"{BASE_URL}/courses/{course_id}/groups"
    groups_response = requests.get(groups_url, headers=headers)
    groups_response.raise_for_status()
    groups = groups_response.json()
    
    # Get group memberships
    memberships_url = f"{BASE_URL}/courses/{course_id}/group_categories"
    memberships_response = requests.get(memberships_url, headers=headers)
    memberships_response.raise_for_status()
    group_categories = memberships_response.json()
    
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
    
    return {
        "students": student_group_info,
        "groups": groups,
        "group_categories": group_categories
    }
