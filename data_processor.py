import pandas as pd
import os
from tempfile import mkstemp

def process_and_export_data(data):
    students_df = pd.DataFrame(data["students"])
    students_df["groups"] = students_df["groups"].apply(lambda x: ", ".join(x) if x else "No Group")
    
    groups_df = pd.DataFrame(data["groups"])
    
    # Create a temporary file
    fd, temp_path = mkstemp(suffix='.csv')
    os.close(fd)
    
    try:
        with open(temp_path, 'w', newline='') as csvfile:
            students_df.to_csv(csvfile, index=False)
            csvfile.write('\n')  # Add a blank line between tables
            groups_df.to_csv(csvfile, index=False)
        
        return temp_path
    except Exception as e:
        os.unlink(temp_path)
        raise RuntimeError(f"Error while creating CSV file: {str(e)}")
