import pandas as pd
import os
from tempfile import NamedTemporaryFile

def process_and_export_data(data):
    students_df = pd.DataFrame(data["students"])
    students_df["groups"] = students_df["groups"].apply(lambda x: ", ".join(x) if x else "No Group")
    
    groups_df = pd.DataFrame(data["groups"])
    group_categories_df = pd.DataFrame(data["group_categories"])
    
    with NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        students_df.to_csv(temp_file.name, index=False)
        groups_df.to_csv(temp_file.name, mode='a', index=False)
        group_categories_df.to_csv(temp_file.name, mode='a', index=False)
    
    return temp_file.name
