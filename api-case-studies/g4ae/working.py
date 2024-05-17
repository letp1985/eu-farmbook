from metadata_processing.process_metadata import ExcelDataProcessor
from auth.token_management import get_token
from dotenv import load_dotenv
import os

# get environment variables
load_dotenv()
API_ADDRESS = os.environ.get("API_ADDRESS")
project_id = os.environ.get("PROJECT_ID")

metadata_folder_path = "data"
metadata_file_name = "D2.2_List of indicators for self-assessment.xlsm"
metadata_file_path = os.path.join(metadata_folder_path, metadata_file_name)
ko_folder_path = "data/kos/"



def process_metadata():
    """
    Processes the metadata from the metadata_file_path variable set on the top of the script
    See process_metadata.py for more details
    """
    processor = ExcelDataProcessor(metadata_file_path)
    processor.pivot_table()
    processor.rename_columns()
    processor.remove_columns()
    processor.convert_creators_columns()
    processor.convert_list_properties()
    df = processor.df
    return df


print(process_metadata().transpose())