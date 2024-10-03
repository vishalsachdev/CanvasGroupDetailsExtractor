import pandas as pd
import os
from tempfile import mkstemp
import logging

logger = logging.getLogger(__name__)

def process_and_export_data(data):
    logger.info("Starting data processing and export")
    students_df = pd.DataFrame(data["students"])
    students_df["groups"] = students_df["groups"].apply(lambda x: ", ".join(x) if x else "No Group")
    
    groups_df = pd.DataFrame(data["groups"])
    
    logger.info(f"Processed {len(students_df)} students and {len(groups_df)} groups")

    # Create a temporary file
    fd, temp_path = mkstemp(suffix='.csv')
    os.close(fd)
    
    logger.info(f"Created temporary file: {temp_path}")
    
    try:
        with open(temp_path, 'w', newline='') as csvfile:
            students_df.to_csv(csvfile, index=False)
            csvfile.write('\n')  # Add a blank line between tables
            groups_df.to_csv(csvfile, index=False)
        
        logger.info(f"Data written to temporary file: {temp_path}")
        return temp_path
    except Exception as e:
        logger.error(f"Error while creating CSV file: {str(e)}")
        try:
            os.unlink(temp_path)
            logger.info(f"Temporary file {temp_path} removed due to error")
        except Exception as remove_error:
            logger.error(f"Error removing temporary file {temp_path}: {str(remove_error)}")
        raise RuntimeError(f"Error while creating CSV file: {str(e)}")
